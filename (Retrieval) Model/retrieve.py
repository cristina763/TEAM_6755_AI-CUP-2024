import os
import json
import argparse
from tqdm import tqdm
import pdfplumber
import pytesseract
from PIL import Image
from rank_bm25 import BM25Plus
from ckiptagger import WS
import re

# 初始化 CkipTagger 的 WS（Word Segmentation）模組
ws = WS("../Preprocess/data")  # 載入剛下載的模型

def convert_to_western_year(text):
    """
    將文本中的民國年轉換為西元年。

    Args:
        text (str): 包含民國年的文字。

    Returns:
        str: 將民國年轉換為西元年的文字。
    """
    def taiwan_to_western(year):
        """
        將民國年數轉換為西元年數。

        Args:
            year (int): 民國年份。

        Returns:
            int: 對應的西元年份。
        """
        if 1 <= year < 200:  # 假設民國年不超過 200 年
            return year + 1911
        return year
    
    text = re.sub(r'民國(\d{2,3})年', lambda m: f"{taiwan_to_western(int(m.group(1)))}年", text)
    return text

def clean_text(text):
    """
    清理文本中的多餘字符，僅保留中文和英文字母。

    Args:
        text (str): 要清理的文本。

    Returns:
        str: 清理後的文本，僅包含字母、數字和中文字符。
    """
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\u4e00-\u9fff]+', '', text)
    text = text.lower()
    return text

def generate_mixed_2_3grams(tokens):
    """
    生成 2-gram 和 3-gram 的混合詞組。

    Args:
        tokens (list): 字詞列表。

    Returns:
        list: 由 2-gram 和 3-gram 組成的詞組列表。
    """
    bigrams = [''.join(tokens[i:i+2]) for i in range(len(tokens)-1)]
    trigrams = [''.join(tokens[i:i+3]) for i in range(len(tokens)-2)]
    return bigrams + trigrams

def load_data(source_path):
    """
    載入指定路徑的 PDF 文檔並提取文本內容。

    Args:
        source_path (str): 包含 PDF 文件的資料夾路徑。

    Returns:
        dict: 包含 PDF 文件 ID 和對應文本內容的字典。
    """
    masked_file_ls = os.listdir(source_path)
    corpus_dict = {
        int(file.replace('.pdf', '')): read_pdf(os.path.join(source_path, file))
        for file in tqdm(masked_file_ls) if file.endswith('.pdf')
    }
    return corpus_dict

def read_pdf(pdf_loc):
    """
    讀取單個 PDF 文件並返回其文本內容。

    Args:
        pdf_loc (str): PDF 文件路徑。

    Returns:
        str: PDF 文件中提取並清理後的文本內容。
    """
    pdf_text = ''
    try:
        pdf = pdfplumber.open(pdf_loc)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                cleaned_text = clean_text(text)
                cleaned_text = convert_to_western_year(cleaned_text)
                pdf_text += cleaned_text
            else:
                img = page.to_image(resolution=300).original
                ocr_text = pytesseract.image_to_string(img, lang='chi_tra+eng')
                cleaned_text = clean_text(ocr_text)
                cleaned_text = convert_to_western_year(cleaned_text)
                pdf_text += cleaned_text
        pdf.close()
    except Exception as e:
        print(f"Error reading PDF {pdf_loc}: {e}")
    return pdf_text

def BM25Plus_retrieve(query, source, corpus_dict):
    """
    使用 BM25+ 演算法對查詢文本進行檢索。

    Args:
        query (str): 用戶的查詢文本。
        source (list): 文檔 ID 列表。
        corpus_dict (dict): 包含文檔 ID 和對應文本的字典。

    Returns:
        int: 相似度最高的文檔 ID。
    """
    query = convert_to_western_year(query)
    
    tokenized_corpus = [
        generate_mixed_2_3grams(ws([clean_text(corpus_dict[int(file)])])[0])
        for file in source
    ]
    bm25 = BM25Plus(tokenized_corpus)
    
    tokenized_query = generate_mixed_2_3grams(ws([clean_text(query)])[0])
    
    scores = bm25.get_scores(tokenized_query)
    best_match_idx = scores.argmax()
    return source[best_match_idx]

if __name__ == "__main__":
    """
    程式入口，解析命令列參數，載入資料並執行文本檢索。
    """
    parser = argparse.ArgumentParser(description='Process some paths and files.')
    parser.add_argument('--question_path', type=str, required=True, help='讀取發布題目路徑')
    parser.add_argument('--source_path', type=str, required=True, help='讀取參考資料路徑')
    parser.add_argument('--output_path', type=str, required=True, help='輸出符合參賽格式的答案路徑')
    args = parser.parse_args()

    answer_dict = {"answers": []}
    with open(args.question_path, 'rb') as f:
        qs_ref = json.load(f)

    source_path_insurance = os.path.join(args.source_path, 'insurance')
    corpus_dict_insurance = load_data(source_path_insurance)
    
    source_path_finance = os.path.join(args.source_path, 'finance')
    corpus_dict_finance = load_data(source_path_finance)
    
    with open(os.path.join(args.source_path, 'faq/pid_map_content.json'), 'rb') as f_s:
        key_to_source_dict = json.load(f_s)
        key_to_source_dict = {int(key): value for key, value in key_to_source_dict.items()}

    for q_dict in qs_ref['questions']:
        if q_dict['category'] == 'finance':
            retrieved = BM25Plus_retrieve(q_dict['query'], q_dict['source'], corpus_dict_finance)
            answer_dict['answers'].append({"qid": q_dict['qid'], "retrieve": retrieved})
        elif q_dict['category'] == 'insurance':
            retrieved = BM25Plus_retrieve(q_dict['query'], q_dict['source'], corpus_dict_insurance)
            answer_dict['answers'].append({"qid": q_dict['qid'], "retrieve": retrieved})
        elif q_dict['category'] == 'faq':
            corpus_dict_faq = {key: str(value) for key, value in key_to_source_dict.items() if key in q_dict['source']}
            retrieved = BM25Plus_retrieve(q_dict['query'], q_dict['source'], corpus_dict_faq)
            answer_dict['answers'].append({"qid": q_dict['qid'], "retrieve": retrieved})
        else:
            raise ValueError("Unknown category")

    with open(args.output_path, 'w', encoding='utf8') as f:
        json.dump(answer_dict, f, ensure_ascii=False, indent=4)

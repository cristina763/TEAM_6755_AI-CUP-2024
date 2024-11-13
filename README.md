# TEAM_6755
**Python版本為3.10**  
____
cd至 *{path}\TEAM_6755_AI-CUP-2024-main* 底下並install package  

執行指令  
```
pip install -r requirements.txt
```

**argparse**:用於解析命令列參數  
**tqdm**:用於顯示執行進度  
**pdfplumber**:用於處理和提取 PDF 文檔內容  
**pytesseract**:使用 OCR（光學字符識別）從圖片中提取文本。當 PDF 頁面沒有文本時，將頁面轉為圖片並使用 pytesseract 來識別圖片中的文字  
**Pillow**:用於處理和操作圖像  
**rank_bm25**:用於文本檢索  
**ckiptagger**:用於中文分詞  
**gdown**:從Google Drive下載檔案  
**tensorflow==2.11.0**:ckiptagger 依賴 TensorFlow  
**numpy==1.21.6**:供 TensorFlow 等package使用  

## Preprocess file  
1. cd至 *{path}\TEAM_6755_AI-CUP-2024-main\Preprocess* 執行ckitagger_data.py  
2. 執行tesseract-ocr-w64-setup-v5.3.0.20221214.exe，並將chi_tra.traineddata語言資料包加進 *{path}\Tesseract-OCR\tessdata\\*  
3. 到PATH添加環境變數 *{path}\Tesseract-OCR* 和 *{path}\Tesseract-OCR\tessdata*
____
preprocess file中的ckiptagger分詞與提取pdf圖片文字的OCR都安裝完畢且添加完環境變數之後  
cd至 *{path}\TEAM_6755_AI-CUP-2024-main\\(Retrieval) Model\\*  

執行指令  
```
python retrieve.py --question_path {path}/競賽資料集/dataset/preliminary/questions_preliminary.json --source_path {path}/競賽資料集/reference --output_path {path}/競賽資料集/dataset/preliminary/pred_retrieve.json
```
{path}改為執行者的(主辦方提供的)競賽資料集路徑  

***由於我們使用的策略如果將preprocess與檢索演算法分開執行會使準確率降低，因此只需執行一個python檔即可得出預測檢索結果***

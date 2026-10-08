# TEAM_6755

## 專案摘要

- **程式庫紀錄日期：** 2024-11-13
- **競賽名稱：** AI CUP 2024 玉山人工智慧公開挑戰賽－RAG 與 LLM 在金融問答的應用
- **參賽隊伍：** TEAM 6755
- **初賽排名：** 36/218 (獲前標獎項)
- **任務類型：** 金融文件檢索（Retrieval）
- **相關連結：** [AI CUP 2024 官方頁面與得獎名單](https://www.aicup.tw/ai-cup-2024-competition)

競賽要求從主辦方提供的金融、保險與 FAQ 語料中，找出最能回答問題的來源文件，本專案聚焦 Retrieval 階段：將不同格式的 PDF 與文字資料轉換成可搜尋語料，計算問題與候選文件的相關性，最後輸出競賽指定的文件編號。

## 解題思路

金融文件同時包含文字型 PDF、掃描圖片、民國年日期與中文專有名詞，直接比對原始文字容易因內容無法擷取或表示方式不同而漏掉相關文件。為處理這些問題，本專案：

1. 優先以 `pdfplumber` 讀取 PDF 文字層，無文字層時改用 Tesseract OCR，避免掃描頁面被忽略。
2. 清理文件內容並將民國年轉換為西元年，統一日期格式。
3. 使用 CKIPTagger 進行中文斷詞，再加入混合 2-gram／3-gram，補足斷詞誤差並保留相鄰詞彙資訊。
4. 依 finance、insurance、faq 分別建立語料，縮小每次檢索的候選範圍。
5. 使用 BM25+ 排序候選文件；此方法不需額外訓練模型，能快速重現結果並檢查各文件的相關性分數。
6. 將前處理與檢索整合為同一執行流程，確保實際推論使用一致的文字處理方式。

## 競賽資料

主辦方資料包含問題 JSON，以及 finance、insurance、faq 三類參考語料。

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

## (Retrieval) Model
preprocess file中的ckiptagger分詞與提取pdf圖片文字的OCR都安裝完畢且添加完環境變數之後  
cd至 *{path}\TEAM_6755_AI-CUP-2024-main\\(Retrieval) Model\\*  

執行指令  
```
python retrieve.py --question_path {path}/競賽資料集/dataset/preliminary/questions_preliminary.json --source_path {path}/競賽資料集/reference --output_path {path}/競賽資料集/dataset/preliminary/pred_retrieve.json
```
{path}改為執行者的(主辦方提供的)競賽資料集路徑  

***由於我們使用的策略如果將preprocess與檢索演算法分開執行會使準確率降低，因此只需執行一個python檔即可得出預測檢索結果***

至Preprocess file
1.執行ckitagger_data.py
2.執行tesseract-ocr-w64-setup-v5.3.0.20221214.exe，並將chi_tra.traineddata語言資料包加進C:\Program Files\Tesseract-OCR\tessdata\
3.到PATH添加環境變數C:\Program Files\Tesseract-OCR 和 C:\Program Files\Tesseract-OCR\tessdata

preprocess file中的ckiptagger分詞與提取pdf圖片文字的OCR都安裝完畢且添加完環境變數之後  
cd至\TEAM_6755_AI-CUP-2024-main\\(Retrieval) Model\  
執行指令python retrieve.py  --question_path {your path}/競賽資料集/dataset/preliminary/questions_preliminary.json --source_path {your path}/競賽資料集/reference --output_path {your path}/競賽資料集/dataset/preliminary/pred_retrieve.json

**由於我們使用的策略如果將preprocess與檢索演算法分開執行會使準確率降低，因此只需執行一個python檔即可得出預測檢索結果**

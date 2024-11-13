cd至\TEAM_6755_AI-CUP-2024-main\\(Retrieval) Model\  
執行指令python retrieve.py  --question_path {your path}/競賽資料集/dataset/preliminary/questions_preliminary.json --source_path {your path}/競賽資料集/reference --output_path {your path}/競賽資料集/dataset/preliminary/pred_retrieve.json

**由於我們使用的策略如果將preprocess與檢索演算法分開執行會使準確率降低，因此只需執行一個python檔即可得出預測檢索結果**

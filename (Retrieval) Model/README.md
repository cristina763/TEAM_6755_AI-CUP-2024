preprocess file中的ckiptagger分詞與提取pdf圖片文字的OCR都安裝完畢且添加完環境變數之後  

執行retrieve.py  
指令:  
```
python retrieve.py --question_path {path}/競賽資料集/dataset/preliminary/questions_preliminary.json --source_path {path}/競賽資料集/reference --output_path {path}/競賽資料集/dataset/preliminary/pred_retrieve.json
```
{path}改為執行者的(主辦方提供的)競賽資料集路徑  

**question_path**: 提供問題的JSON檔案路徑。  
**source_path**: 需要檢索的參考資料的路徑(包含reference中的faq, finance, insurance)。  
**output_path**: 產⽣的預測答案將被儲存在這個路徑中。

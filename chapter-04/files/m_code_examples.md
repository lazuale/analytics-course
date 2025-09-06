# 📊 M-код примеры для Главы 4

## Базовое подключение к CSV
```m
let
    Source = Csv.Document(File.Contents("C:\data\file.csv"), [Delimiter=";", Encoding=65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    Headers
```

## Очистка текстовых данных  
```m
let
    Source = Excel.CurrentWorkbook(){[Name="RawData"]}[Content],
    CleanText = Table.TransformColumns(Source, {
        {"CustomerName", each Text.Proper(Text.Trim(_)), type text},
        {"Email", each Text.Lower(Text.Trim(_)), type text}
    })
in
    CleanText
```

## Объединение таблиц
```m
let
    Sales = Excel.CurrentWorkbook(){[Name="Sales"]}[Content],
    Products = Excel.CurrentWorkbook(){[Name="Products"]}[Content],
    Merged = Table.NestedJoin(Sales, {"ProductID"}, Products, {"ProductID"}, "ProductInfo", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "ProductInfo", {"ProductName", "Category"})
in
    Expanded
```

## Параметризованный запрос
```m
let
    FilePath = Parameter_Path & Parameter_FileName,
    Source = Csv.Document(File.Contents(FilePath), [Delimiter=";", Encoding=65001]),
    Processed = Table.TransformColumnTypes(Source, {{"Date", type date}, {"Amount", type number}})
in
    Processed
```

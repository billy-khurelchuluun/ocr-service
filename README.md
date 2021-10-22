# ocr-service

A simple service that takes image/pdf URL, parses into text response. Uses google-tesseract and its python wrapper pytesseract for OCR engine.

# Endpoint

POST /parse
```
{
  "docType":"image/pdf"
  "url":"{{URL}}",
  "crop":true/false,
  "cropBox":"{{coordinates}}"
}
```
# Examples

Import postman collection into Postman to try.

## Адаптация метода границ Канни для подсчёта количества бактерий на изображениях, получаемых с помощью цифрового микроскопа. Реализация Flask API для подсчета бактерий

```http
host = ip:5000 
```
To view uuid all uploaded images.
```http
GET http://host/images
```
```json
{
    "images": [
        "7cc39d16-6197-44cf-a14c-ef58b7585882"
    ],
    "processed_images": [
        "68288845-6444-41e9-aa08-d8f6d39e519b",
        "b7f4f878-202b-4c31-b754-e162349406f3"
    ]
}
```
To upload image.
```http
POST http://host/images/upload
```
```
200 OK
```
To count bacillus on image by uuid.
```http
POST http://host/images/{image_uuid}/count
```
```
202 ACCEPTED
```
To download processed image by image uuid.
```http
GET http://host/images/{image_uuid}/download
```
To view all jobs.
```http
GET http://host/counts
```
```json
[
    {
        "cause": "",
        "status": "Status.COMPLETED",
        "uuid": "b638250a-14f8-45b2-9dd7-5291a5770b9d"
    },
    {
        "cause": "Image not found with UUID 68288845-6444-41e9-aa08-d8f6d39e519b",
        "status": "Status.ERROR",
        "uuid": "1e76cbd5-0795-463f-ab0d-f1e2fa0dd4bd"
    },
    {
        "cause": "",
        "status": "Status.RUNNING",
        "uuid": "b434b961-2657-4edd-b1d7-b27f90b80e8b"
    }
]
```
To view job by uuid.
```http
GET http://host/counts/{job_uuid}
```
```json
 {
  "cause": "",
  "status": "Status.COMPLETED",
  "uuid": "b638250a-14f8-45b2-9dd7-5291a5770b9d"
}
```
To download processed image by job uuid.
```http
GET http://host/counts/{job_uuid}/image/download
```

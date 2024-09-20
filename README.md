# micro-api

## Ejemplos

Importa módulo

```python
from micro import api
gateway = api.Client()
```

Subir Archivos

```python
gateway.post("/api/files", files={
  'file': ("example.pdf", filedata, 'application/pdf')
})  
```      

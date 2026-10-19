# Automatizar metadatos Zenodo

## 1. Token (solo en tu máquina)

1. Entra en https://zenodo.org/account/settings/applications/tokens    
2. New token. Nombre: `grok-metadata-2026`.    
3. Scope: **deposit:write** (y `deposit:actions` si más adelante publicas borradores).    
4. Copia el token. No lo pegues en el chat ni en Drive.

```bash  
export ZENODO_TOKEN='pegahere'  
```

Sandbox de pruebas: `https://sandbox.zenodo.org` + token de sandbox +    
`export ZENODO_API=https://sandbox.zenodo.org/api`

## 2. Comandos

```bash  
cd zenodo_api   # o la ruta donde copies estos archivos  
python3 zenodo_update.py list      # depositions de TU cuenta  
python3 zenodo_update.py diff      # ahora vs propuesto (no necesita write)  
python3 zenodo_update.py apply --dry-run  
python3 zenodo_update.py apply     # escribe los 15  
```

`diff` usa la API pública y no cambia nada.    
`apply` exige que los 15 DOI pertenezcan a la cuenta del token.

## 3. Qué cambia

Título, creator (`López Paz, Lázaro` + afiliación independiente), licencia CC-BY-4.0 (MIT solo en Canelone), keywords, descripción con Estado/Evidencia, `related_identifiers` entre los 15.

No toca ficheros. El DOI se mantiene.

## 4. Si un record no aparece en `list`

Está publicado con otra cuenta o es un record ajeno. El script hace `SKIP`.

## 5. Curl equivalente (un record)

```bash  
curl -X PUT "https://zenodo.org/api/deposit/depositions/RECORD_ID" \  
  -H "Authorization: Bearer $ZENODO_TOKEN" \  
  -H "Content-Type: application/json" \  
  -d '{"metadata":{"title":"...","upload_type":"publication","publication_type":"technicalnote","license":"cc-by-4.0","creators":[{"name":"López Paz, Lázaro","affiliation":"Investigador independiente, El Prat de Llobregat, Barcelona, España"}],"description":"...","keywords":["..."],"language":"spa"}}'  
```

El `RECORD_ID` de depósito suele coincidir con el id público (`20761277`, etc.).  

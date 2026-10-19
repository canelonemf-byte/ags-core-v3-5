# Instrucciones de corrección — metadatos Zenodo / DataCite

Autor de los trabajos: **López Paz, Lázaro**    
Afiliación: Investigador independiente, El Prat de Llobregat, Barcelona, España    
Fecha de esta guía: 2026-08-30

Los 15 DOI están `findable`. El fallo no es el archivo: es el campo **creator**. DataCite los ha clasificado como `nameType: Organizational` y les ha colgado ROR/ISNI de BIST, IAC, ISDEFE, Fundación Medina, PERSEI, IN2UB, etc.

## Qué hay que dejar en los 15

```  
Family name:  López Paz  
Given names:  Lázaro  
Affiliation:  Investigador independiente, El Prat de Llobregat, Barcelona, España  
ORCID:        (vacío hasta que exista el tuyo)  
License:      CC-BY-4.0   (MIT solo en Canelone, 21513673)  
```

Un solo autor. Cero instituciones en el nombre.

Lista de DOI:

```  
10.5281/zenodo.20761277  
10.5281/zenodo.20812704  
10.5281/zenodo.21238123  
10.5281/zenodo.21321630  
10.5281/zenodo.21345185  
10.5281/zenodo.21361772  
10.5281/zenodo.21401153  
10.5281/zenodo.21513673  
10.5281/zenodo.21640446  
10.5281/zenodo.21721963  
10.5281/zenodo.21806526  
10.5281/zenodo.22028729  
10.5281/zenodo.22131030  
10.5281/zenodo.22131440  
10.5281/zenodo.22150378  
```

---

## Vía A — interfaz web (sin script)

1. Entra en https://zenodo.org e inicia sesión en **la cuenta que publicó** esos records.  
2. Abre `https://zenodo.org/records/22131030` (cambia el id).  
3. Botón **Edit**.  
4. En *Creators / Authors*:  
   - Borra **todas** las filas (en `21401153` hay dos PERSEI).  
   - *Add creator*:  
     - Family name: `López Paz`  
     - Given names: `Lázaro`  
     - Affiliation: `Investigador independiente, El Prat de Llobregat, Barcelona, España`  
     - ORCID: vacío  
5. Licencia: `Creative Commons Attribution 4.0` (no Apache, no APL).  
   En `22150378` añade una licencia; ahora no tiene.  
6. **Save**. No hace falta *New version*. El DOI no cambia.

Prioridad si no puedes hacer los 15 seguidos:

1. `21721963` (ISDEFE)    
2. `21640446` (IAC)    
3. `22131030` y `22028729` (BIST)    
4. `21401153` (PERSEI ×2)    
5. `21321630` (SECOT + instituto japonés)    
6. El resto  

Títulos, keywords y descripción se pueden dejar para una segunda pasada (Vía B).

---

## Vía B — API / scripts (recomendado)

Token: https://zenodo.org/account/settings/applications/tokens    
Scopes: `deposit:write` (metadatos). `deposit:actions` solo si más adelante versionas ficheros.

```bash  
export ZENODO_TOKEN='...'     # no lo pegues en chats ni en Drive

# 1. Ensayo  
python3 zenodo_apply_all.py --authors-only

# 2. Si no hay SKIP: escribe autores  
python3 zenodo_apply_all.py --apply --authors-only

# 3. Título, licencia, descripción, related_identifiers  
python3 zenodo_apply_all.py --apply

# 4. Comprobar  
python3 zenodo_validate.py --fail-on error  
python3 datacite_validate.py  
```

Archivos (carpeta NotebookLM_Fuentes / `zenodo_api`):

- `zenodo_apply_all.py` — orquestador    
- `zenodo_metadata.json` — valores objetivo    
- `zenodo_validate.py` — reglas Zenodo    
- `datacite_validate.py` — registro DataCite    
- `ejemplo_validar_y_corregir.py` — un solo DOI    
- `ejemplo_orcid_doi.py` — cuando exista ORCID  

PUT que ejecuta el script:

```  
PUT https://zenodo.org/api/deposit/depositions/{id}  
Authorization: Bearer $ZENODO_TOKEN  
Content-Type: application/json

{  
  "metadata": {  
    "creators": [{  
      "name": "López Paz, Lázaro",  
      "affiliation": "Investigador independiente, El Prat de Llobregat, Barcelona, España"  
    }]  
  }  
}  
```

El resto de campos se conserva si usas `--authors-only`.

---

## Vía C — un DOI a mano con Python

```bash  
python3 ejemplo_validar_y_corregir.py 22131030  
ZENODO_TOKEN='...' python3 ejemplo_validar_y_corregir.py 22131030 --apply  
```

---

## Comprobar que DataCite se actualizó

Zenodo reexporta a DataCite en minutos u horas. No editas DataCite a mano.

```bash  
python3 datacite_validate.py  
curl -s -H "Accept: application/vnd.api+json" \  
  https://api.datacite.org/dois/10.5281/zenodo.22131030 \  
  | python3 -c "import sys,json; a=json.load(sys.stdin)['data']['attributes'];  
print(a['creators']); print(a.get('rightsList'))"  
```

Objetivo por record:

- `state`: findable    
- `creators[0].name`: `López Paz, Lázaro`    
- `creators[0].nameType`: **Personal** (no Organizational)    
- sin ROR/ISNI de BIST, IAC, ISDEFE, IIQ…    
- `rightsList` CC-BY-4.0  

Si DataCite sigue en Organizational a las 24 h, vuelve a *Edit → Save* en Zenodo para forzar el reenvío.

---

## ORCID (después de tener iD propio)

1. Alta: https://orcid.org/register    
2. `export ZENODO_ORCID=0000-000X-XXXX-XXXX`    
3. `python3 ejemplo_orcid_doi.py 22131030 --apply` o un `--apply` completo.    
4. Zenodo → perfil → Linked accounts → ORCID.    
5. En ORCID: Add work → DOI de cada record.

No uses ORCID de homónimos (Sara A. López-Paz, Iván Lopez Paz, Miguel Lázaro López-Villaseñor).

---

## Lo que esta corrección NO hace

- No cambia ficheros ni el DOI.    
- No quita `noteboo.txt` ni el ZIP de 172 MB (`zenodo_files.py newversion`).    
- No publica en Academia.edu.    
- No crea el ORCID.

---

## Criterio de «cerrado»

`python3 zenodo_validate.py` → 0 errores de creator/licencia.    
`python3 datacite_validate.py` → `nameType=Personal` en los 15, sin ROR institucional en el autor.  

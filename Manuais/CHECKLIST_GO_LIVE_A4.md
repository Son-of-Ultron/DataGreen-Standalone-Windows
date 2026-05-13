# DataGreen — Checklist Final de Entrega (A4)

**Objetivo:** validar em ~10 minutos antes de entregar ao jardineiro.  
**Modo:** stand-alone local (SQLite).  
**URL local:** `http://127.0.0.1:8765`

---

## 1) Seguranca minima (obrigatorio)

- [ ] Trocar senha do dono
- [ ] Trocar senha do contador
- [ ] Confirmar `DATAGREEN_DESKTOP=1`
- [ ] Confirmar `USE_SQLITE=1`
- [ ] Confirmar `DJANGO_SECRET_KEY` personalizada

### Comandos (Linux)
```bash
cd backend
.venv/bin/python manage.py changepassword dono
.venv/bin/python manage.py changepassword contador
```

### Comandos (Windows)
```bat
cd backend
.venv\Scripts\python.exe manage.py changepassword dono
.venv\Scripts\python.exe manage.py changepassword contador
```

---

## 2) Subir o sistema

- [ ] Backend inicia sem erro
- [ ] Sistema abre no navegador

### Linux
```bash
cd /caminho/datagreen
./start_datagreen.sh
```

### Windows
```bat
cd C:\caminho\datagreen
start_datagreen.bat
```

---

## 3) Teste funcional rapido

### Com usuario **dono**
- [ ] Criar 1 cliente
- [ ] Criar 1 contrato
- [ ] Criar 1 lancamento financeiro
- [ ] Cancelar 1 lancamento

### Com usuario **contador**
- [ ] Consegue visualizar dados
- [ ] Nao consegue criar/editar/excluir

---

## 4) Exportacoes

- [ ] Exportar CSV mensal
- [ ] Exportar XLSX mensal
- [ ] Exportar Excel completo
- [ ] Confirmar download dos arquivos

---

## 5) Backup e restauracao

- [ ] Gerar backup manual
- [ ] Confirmar arquivo em `backups/`
- [ ] Testar restauracao com backup conhecido
- [ ] Confirmar que restauracao cria backup previo

### Comandos (Linux)
```bash
cd backend
.venv/bin/python manage.py backup_sqlite
.venv/bin/python manage.py restore_sqlite /caminho/do/backup.sqlite3
```

### Comandos (Windows)
```bat
cd backend
.venv\Scripts\python.exe manage.py backup_sqlite
.venv\Scripts\python.exe manage.py restore_sqlite C:\caminho\do\backup.sqlite3
```

---

## 6) Encerramento seguro

- [ ] Fechar servidor com `Ctrl + C` (ou bandeja no Windows)
- [ ] Confirmar encerramento sem erro

---

## Go/No-Go (decisao final)

**Pode entregar ao usuario final se TODOS itens estiverem marcados.**

- [ ] GO-LIVE APROVADO
- Responsavel:
- Data:
- Observacoes:


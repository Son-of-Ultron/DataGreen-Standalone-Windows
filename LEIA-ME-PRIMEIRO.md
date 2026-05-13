# DataGreen — versão stand-alone para Windows

Este pacote foi preparado para uso local em um único computador. Ele não depende de publicação web e foi montado com o frontend já compilado em `dist/public`, backend Django em modo desktop, banco SQLite local e scripts simples para instalação, abertura diária, backup manual e troca de senha.

## Como usar pela primeira vez

Na primeira execução, abra a pasta do DataGreen e dê duplo clique em `1-INSTALAR-PRIMEIRA-VEZ.bat
(Esse passo prepara o Python, instala as dependências necessárias e deixa o sistema pronto para abrir localmente)

Em seguida, execute `2-INICIAR-DATAGREEN.bat`.

Quando o DataGreen abrir, acesse o endereço local mostrado pelo programa, normalmente `http://127.0.0.1:8765`. O primeiro usuário administrativo é criado automaticamente na primeira inicialização.

## Instalação em 1 executável (recomendado para cliente final)

Você também pode entregar um instalador único do Windows (`.exe`) que:
- copia todos os arquivos para `C:\Program Files\DataGreen`;
- cria atalhos no Menu Iniciar e opcionalmente na Área de Trabalho;
- oferece executar a primeira configuração automaticamente ao final.

Para gerar esse instalador no computador de desenvolvimento:

1. Dê duplo clique em `5-GERAR-INSTALADOR.bat`.
2. Aguarde a compilação do Inno Setup (o script tenta instalar o Inno automaticamente via `winget` se necessário).
3. Pegue o arquivo final em `release\installer\DataGreen_Setup.exe`.

Se o seu ambiente de desenvolvimento for Linux (ex.: Linux Mint), use o workflow do GitHub:

1. Envie o projeto para o GitHub.
2. Abra `Actions` -> `Build Windows Installer` -> `Run workflow`.
3. Baixe o artefato `datagreen-windows-installer` ao final do build.

**Importante:** o GitHub só empacota o que está **commitado** no repositório. Se o workflow falhar com “arquivo não existe” ou o passo “Verify files required…” listar faltas, faça commit de `backend/`, `dist/public/`, `windows/` e dos `.bat` da raiz, depois `git push`.

```bash
cd "/caminho/para/DataGreen-Standalone-Windows"
git add backend/ dist/public/ windows/ Manuais/ .github/ \
  1-INSTALAR-PRIMEIRA-VEZ.bat 2-INICIAR-DATAGREEN.bat \
  3-BACKUP-MANUAL.bat 4-TROCAR-SENHA.bat \
  5-GERAR-INSTALADOR.bat LEIA-ME-PRIMEIRO.md .gitignore
git status
git commit -m "Incluir arquivos do app para build do instalador Windows"
git push
```

No computador do cliente:

1. Executar `DataGreen_Setup.exe`.
2. Ao concluir, marcar "Executar primeira configuração agora" (recomendado).
3. Depois usar o atalho `DataGreen` normalmente.

| Item | Valor inicial |
|---|---|
| Usuário principal | `dono` |
| Senha temporária | `dono123` |
| Usuário auxiliar | `contador` |
| Senha temporária | `contador123` |
| Endereço local | `http://127.0.0.1:8765` |

## Troca obrigatória da senha inicial

As senhas acima são **temporárias**. Depois do primeiro acesso, execute `4-TROCAR-SENHA.bat` e altere pelo menos a senha do usuário `dono`. Guarde a nova senha em local seguro, pois o sistema roda localmente e não há recuperação automática por e-mail.

## Uso diário

Depois da primeira configuração, use apenas `2-INICIAR-DATAGREEN.bat`. O sistema abrirá em modo local e os dados ficarão gravados no arquivo `backend/db.sqlite3`, dentro desta pasta.

## Backup

O sistema possui rotina de backup SQLite. Para fazer um backup manual, dê duplo clique em `3-BACKUP-MANUAL.bat`. Os arquivos de backup são salvos na pasta configurada pelo backend, normalmente em `backend/backups`, com nome contendo data e hora.

Recomenda-se copiar periodicamente os backups para Google Drive, HD externo ou pasta sincronizada. O arquivo mais importante do sistema é o banco `backend/db.sqlite3`; sem backup, perda do computador ou exclusão da pasta pode causar perda dos dados.

## O que este pacote contém

| Pasta ou arquivo | Finalidade |
|---|---|
| `dist/public` | Interface já compilada para o modo stand-alone. |
| `backend` | Backend Django, modelos, migrações, backup e banco local SQLite gerado no primeiro uso. |
| `windows` | Scripts auxiliares para configuração e abertura em Windows. |
| `1-INSTALAR-PRIMEIRA-VEZ.bat` | Preparação inicial. |
| `2-INICIAR-DATAGREEN.bat` | Abertura diária. |
| `3-BACKUP-MANUAL.bat` | Backup manual. |
| `4-TROCAR-SENHA.bat` | Alteração da senha local. |
| `Manuais` | Documentos complementares do projeto. |

## Observações importantes

Este pacote foi limpo para não carregar `node_modules`, ambiente virtual de desenvolvimento, banco antigo, backups antigos ou pasta de build de desenvolvimento. Na primeira instalação, o computador precisa ter Python funcional e, se as dependências ainda não estiverem instaladas, acesso à internet para baixar os pacotes Python. Depois disso, o uso diário é local.

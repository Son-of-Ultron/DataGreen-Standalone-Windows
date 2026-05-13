# DataGreen no Windows — receita para usar no **seu** PC (atalho + bandeja)

Este texto é uma **receita de bolo** para quem vai usar o DataGreen **só no Windows de casa ou do escritório**, **sem** ficar digitando comando no terminal no dia a dia.

Se você quer o modo **dois terminais** (como programador), leia **`MANUAL_INSTALACAO_LOCAL.md`**.

---

## Ingredientes

1. **Windows 10 ou 11** (de preferência atualizado).  
2. **Internet** na **primeira configuração** (para baixar coisas).  
3. A **pasta do DataGreen** já “montada” por quem desenvolve (pasta `release\DataGreen` **ou** o que o instalador `.exe` colocou no disco).  
4. **Paciência** na primeira vez.

---

## Palavras que vamos usar

| Palavra | O que é |
|--------|---------|
| **Atalho** | Ícone que você **duas vezes clica** para abrir algo. |
| **Bandeja** | Canto **inferior direito** da tela, perto do **relógio** — ficam ícones pequenos. |
| **Navegador** | Chrome, Edge ou Firefox — onde o “site” do DataGreen abre. |
| **Python** | Um programa que precisa estar no computador para o DataGreen funcionar neste modo. O assistente **`.bat`** tenta instalar ou pede ajuda. |
| **winget** | Ferramenta do Windows (muitas vezes já vem) que **baixa** o Python **automaticamente** se você disser **Sim**. |

---

## O que você vai ver quando tudo funcionar

1. Você dá **duplo clique** num atalho.  
2. O **navegador** abre num endereço parecido com **`http://127.0.0.1:8765`**.  
3. Aparece um **íconezinho** perto do **relógio**.  
4. **Fechar só o navegador** **não** desliga o programa — o ícone continua.  
5. Para **desligar de verdade**: **botão direito** no ícone → **Encerrar DataGreen**.

Se você clicar de novo no atalho **com o programa já ligado**, normalmente **só abre o navegador de novo** (não duplica tudo).

---

## Receita — primeira vez no computador (faça nesta ordem)

### Passo 1 — Achar a pasta certa

Dentro do DataGreen instalado deve existir uma pasta chamada **`windows`**.  
Dentro dela há arquivos terminando em **`.bat`**.

Exemplo de caminho (o seu pode ser outro):

```text
C:\DataGreen\windows
```

### Passo 2 — Abrir a “primeira configuração”

1. Abra a pasta **`windows`**.  
2. Dê **duplo clique** no arquivo **`PrimeiraConfiguracao.bat`**.  
3. Vai abrir uma **janela preta** com letras. **Não feche** até ela pedir ou dizer que acabou.

### Passo 3 — Se aparecer pergunta sobre Python / winget

- Se o computador **ainda não tiver** Python direitinho, pode aparecer: **tentar instalar automaticamente?**  
- Se você tem **internet** e confia no download oficial, pode apertar **S** (Sim).  
- Pode pedir **permissão de administrador** — é normal em alguns PCs.  
- Se **não** tiver winget ou der erro, o próprio arquivo **explica** como instalar o Python à mão no site [python.org](https://www.python.org/downloads/) — marque **Add python.exe to PATH**.

### Passo 4 — Se pedir para rodar o `.bat` de novo

Às vezes, depois de instalar o Python, a janela diz para **fechar** e **abrir de novo** o **`PrimeiraConfiguracao.bat`**.  
Faça isso. Não é erro — é o Windows atualizando o “caminho” do Python.

### Passo 5 — Esperar as três etapas dentro da janela

A janela vai fazendo coisas parecidas com:

1. Atualizar o **pip**  
2. Instalar o **servidor** (Django e companhia)  
3. Instalar o que precisa para o **ícone da bandeja**

Precisa de **internet** nessa hora.

### Passo 6 — Quando ler “Concluído com sucesso”

1. Pode fechar a janela preta (ou apertar uma tecla se ela pedir).  
2. **Daqui para frente**, no dia a dia, você usa outro arquivo (próxima parte).

---

## Receita — todo dia (uso normal)

### Passo 1 — Duplo clique

Abra a pasta **`windows`** e dê **duplo clique** em:

```text
Iniciar DataGreen.bat
```

Ou use o **atalho** “DataGreen” que o instalador colocou no Menu Iniciar / Área de trabalho.

### Passo 2 — Navegador

O navegador deve abrir. Se não abrir, digite na barra de endereço:

```text
http://127.0.0.1:8765
```

### Passo 3 — Entrar no sistema

Se alguém já criou usuários de demonstração:

| Usuário | Senha |
|---------|--------|
| **dono** | **dono123** |
| **contador** | **contador123** |

(Troque depois se for uso sério.)

### Passo 4 — Quando terminar o trabalho

1. **Botão direito** no ícone da **bandeja** → **Encerrar DataGreen**.  
2. Assim o “motor” **para de verdade**.

---

## Se você recebeu o instalador `.exe` (Inno Setup)

1. Rode o **`DataGreen_Setup.exe`** e siga as perguntas (Avançar, Avançar).  
2. Quando terminar, abra o **Menu Iniciar** → pasta **DataGreen**.  
3. Rode primeiro **“DataGreen — primeira configuração”** (é o mesmo espírito do `PrimeiraConfiguracao.bat`).  
4. Depois use o atalho **DataGreen** para o dia a dia.

---

## Se você é quem **monta** a pasta para outra pessoa (desenvolvedor)

1. No PC de trabalho, dê duplo clique em **`5-GERAR-INSTALADOR.bat`**.  
2. O script chama `windows\build-installer.ps1` e tenta encontrar o Inno Setup (`ISCC.exe`).  
3. Se não existir, ele tenta instalar via `winget` automaticamente.  
4. Ao final, o instalador sai em **`release\installer\DataGreen_Setup.exe`**.

### Se você desenvolve em Linux Mint (sem Windows local)

1. Suba o repositório para o GitHub.  
2. Abra a aba **Actions**.  
3. Rode manualmente o workflow **Build Windows Installer**.  
4. Baixe o artefato **datagreen-windows-installer** (contém `DataGreen_Setup.exe`).

---

## Onde ficam os dados e qual porta

- **Porta:** **8765** (só neste modo Windows “um clique”).  
- **Arquivo de dados:** **`backend\db.sqlite3`** dentro da pasta instalada (aparece depois que rodou certo uma vez).  

### Backup (cópia de segurança)

1. **Encerre** pelo ícone da bandeja (**Encerrar DataGreen**).  
2. Copie o arquivo **`db.sqlite3`** para outro lugar (pendrive, nuvem).

---

## Quando der errado (tabela simples)

| O que aparece | O que fazer |
|---------------|-------------|
| Não achou Python | Instale em [python.org](https://www.python.org/downloads/) com **Add to PATH**. Rode **`PrimeiraConfiguracao.bat`** de novo. |
| Pediu para abrir o `.bat` de novo depois do winget | Faça isso. É normal. |
| pip falhou / sem internet | Ligue Wi-Fi. Rode **`PrimeiraConfiguracao.bat`** de novo. |
| Navegador em branco | Espere uns segundos. Olhe se o **ícone da bandeja** está lá. Atualize a página. |
| Outro programa usa a porta 8765 | Peça ajuda — algo ocupou a porta. |
| Esqueci a senha do dono | Quem entende um pouco de terminal pode, na pasta `backend`, usar `python manage.py changepassword dono` (com o mesmo modo “desktop” que o manual técnico descreve). |

---

## O que este modo **não** é

- **Não** é um site na internet para o mundo inteiro — é **só no seu PC**.  
- **Não** manda imposto sozinho — ajuda a **organizar** e **exportar** para o contador.  
- Senhas de teste são **fracas**.

---

## Post-it (cinco linhas)

1. **Uma vez:** `PrimeiraConfiguracao.bat`  
2. **Sempre:** `Iniciar DataGreen.bat`  
3. **Navegador:** `127.0.0.1:8765`  
4. **Ícone na bandeja** = ligado  
5. **Encerrar DataGreen** = desligar

---

## Uso diario em computador local

- Abrir: duplo clique em `Iniciar DataGreen.bat` ou `start_datagreen.bat`.
- Fechar: icone da bandeja -> **Encerrar DataGreen**.
- Dados: `backend\db.sqlite3`.
- Backups: pasta `backups\` (comando tecnico: `python manage.py backup_sqlite` dentro de `backend`).
- Restauracao tecnica: `python manage.py restore_sqlite caminho_do_backup.sqlite3`.
- Nao apagar `db.sqlite3` nem mover a pasta sem copiar backup antes.

---

*Guarde mensagem de erro ou print e peça ajuda a quem preparou o pacote.*

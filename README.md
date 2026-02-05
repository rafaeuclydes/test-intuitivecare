# Test Intuitive Care

## Instruções:
 O desafio foi realizado até a terceira parte.
 Parte 1 e 2:
 - Primeiro rodar o extract-data.py e depois o agregation-data.py.
     - Para rodar os scripts:
         - VS Code - No terminar acesse a pastar onde os scripts estão armazenados a rode com o comando: python .\nomedoaqruivo.py
         - No PyCharm ou outros rode os scripts com os botão 'run'.
      
           Obs: Caso rode em linux pode ser que dependendo da distro como Debian você precise rodar com o ambiente virtual venv. Então rode:
              sudo apt install python3-venv (caso não tenha o venv instalado)
              python3 -m venv venv
              source venv/bin/activate
              python+Versão (ex: python3) nomedoarquivo.py
                    
 - O script extract-data.py gera os arquivos consolidado_despesas.zip e .csv e o agregation-data.py gera o despesas_agregadas.csv e o Teste_Rafae_lEuclydes.zip.

 Parte 3:
 - Contem 3 arquivos que podem ser rodados no PostgresSQL ou VSCode
   - Primeiro precisa criar o banco de dados "intuitivecare", se for realizado no terminal do VSCode seguir os comandos abaixo:
     cd "C:\Program Files\PostgreSQL\16\bin"
     .\psql -U postgres
     No banco (usando essa exata ordem):
     CREATE DATABASE intuitivecare;
     \c intuitivecare
     \i 'CAMINHO/01_ddl_estrutura.sql'
     \i 'CAMINHO/02_importacao_csv.sql'
     \i 'CAMINHO/03_queries_analiticas.sql'
     

## 1. TESTE DE INTEGRAÇÃO COM API PÚBLICA

Trade-off técnico:
R - Processar incrementalmente é a opção mais adequada para o carregamento dos dados, pois com esse método a aplicação utiliza menos memória RAM. Outra questão que justifica o processamento incremental, é que os dado da ANS podem ser volumosos e processar incrementalmente torna o carregamento dos dados mais rápido.Inclusive em PC mais limitados é possível rodar o script sem grandes atrasos.

Análise crítica: Durante a consolidação, você encontrará:
- CNPJs duplicados com razões sociais diferentes
  R - Aqui considerei as razão sociais mais prevalentes, pois pode ter acontecido dessas agencias terem trocado a razão social, e como o CNPJ não muda considerar os nomes mais prevalentes pareceu fazer masi sentido.
- Valores zerados ou negativos
- Trimestres com formatos de data inconsistentes
  R - Fazer um "coerce" dessas datas, forçando a terem os mesmo formato, pois é importante ter um padrão para outros testes.

Nesta parte do desafio observei que as tabelas dos 3 trimestres não tinha CNPJ e Razão social, por isso optei por usar os registros ANS para fazer o join do desafio a seguir e então usei o CNPJ como identficador único.

## 2. TESTE DE TRANSFORMAÇÃO E VALIDAÇÃO DE DADOS

Trade-off técnico:
R - Para CNPJs inválidos, mantive os CNPJ mas marquei como inválido, porque a exclusão desses dados poderia causar alguma perda de dados relevantes, que podem só estar na coluna errada.

Análise crítica: Você encontrará CNPJs no arquivo consolidado que não existem no cadastro (ou vice-versa). Decida como tratar:
- Registros sem match no cadastro
  R - Os registros sem match foram mantidos para fazer a agregação, e posteriormente excluídos, pois esses dados só inflam e não agregam no dados visto que não possuiem CNPJ e Razão social. Alem disso, em pesquisas esses ANS podem estar inativos e os dados se reverem a operadoras ativas.
- CNPJs que aparecem múltiplas vezes no cadastro com dados diferentes
  R - Considerei as modalidade e UF como um conjunto com o CNPJ

Trade-off técnico: 
R - Para o join considerei umsistema hibrido pois na tabela do primeiro desafio não tinha o CNPJ para usar como ID, então usei o ANS como identificador intermediário e no final o CNPJ ficou como ID único das operadores.

Trade-off técnico: 
R - Para ordenação, primeiro decidi fazer a agregação pois ela reduz o volume de dados diminuindo o custo computacional.

## 3. TESTE DE BANCO DE DADOS E ANÁLISE 

Trade-off técnico:
R - Para a normalização utilizei a opção B, pela estrutura dos dados e o alto volume de dados a ANS, utilizando tabelas normalizadas separadas, reduz o custo computacional e aumenta a escalabilidade.

Trade-off técnico:
R - Nos valores monetários optei por INTEGER por ser mais preciso, e nas datas optei por DATE pois é  formato mais coerento para datas.

Análise crítica:
- Valores NULL em campos obrigatórios
  R - Descartados por CPNJ são ID únicos.
- Strings em campos numéricos
  R - Tentei fazer uma conversão, assim evita NaN.


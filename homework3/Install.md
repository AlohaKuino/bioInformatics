## **Инструкция по развертыванию**
**1. Установите Python и pip**
```bash
brew install python
```
**2. Создайте виртуальное окружение**
```bash
python3 -m venv venv
source venv/bin/activate
```
**3. Установите Redun**
```bash
pip install redun==0.27.0
```
**4. Установите биоинформатические инструменты**
```bash
brew install fastqc bwa samtools
```
**5. Склонируйте репозиторий**
```bash
git clone https://github.com/AlohaKuino/bioInformatics.git
```
**6. Перейдите в папку homework3**
```bash
cd /homework3
```
**7. Запустим простой пайплайн через redun** 
```bash
cd scripts
redun run hello_pipeline.py main 
```
как итог получим что-то вроде этого
```bash
(venv) aloha_kuino@alohakuino scripts % redun run hello_pipeline.py main                                   
[redun] redun :: version 0.27.0
[redun] config dir: /Users/aloha_kuino/Documents/bioinf/mapping_quality_pipeline/.redun
[redun] Start Execution b87f595d-817e-4646-a0a0-c19eb7a15869:  redun run hello_pipeline.py main
[redun] Tasks will require namespace soon. Either set namespace in the `@task` decorator or with the module-level variable `redun_namespace`.
tasks needing namespace: hello_pipeline.py:add, hello_pipeline.py:main
[redun] Run    Job b0b8607e:  main() on default
[redun] Run    Job 9fe0aaae:  add(a=2, b=3) on default
[redun] 
[redun] | JOB STATUS 2025/05/26 04:21:23
[redun] | TASK    PENDING RUNNING  FAILED  CACHED    DONE   TOTAL
[redun] | 
[redun] | ALL           0       0       0       0       2       2
[redun] | add           0       0       0       0       1       1
[redun] | main          0       0       0       0       1       1
[redun] 
[redun] 
[redun] Execution duration: 0.03 seconds
5
```
**8. Попробуем что-то посерьезнее и запустим основной пайплайн**
```bash
cd ..
redun run pipeline.py main
```
Пайплайн начнет работу, он будет генерить файлы, писать логи. Работает примерно 5-10 минут, по итогу получаем вывод, похожий на вывод простого пайплайна и много полезных файлов

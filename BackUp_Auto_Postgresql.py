# Passo 1 - Importar os módulos necessários
import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import datetime

# Passo 2 - Configurar as credenciais de email
email_user = 'teste@gmail.com'
email_password = '****'

# Passo 3 - Configurar as informações do banco de dados
db_name = 'postgres'
db_user = 'postgres'
db_host = 'localhost'
db_port = '5432' #PORT = '5432'

# Passo 4 - Lê a senha do banco de dados do ambiente
db_password = os.environ.get('1234')

# Passo 5 - Definir o caminho para salvar o arquivo de backup
backup_path = 'C:\\Program Files\\PostgreSQL\\15\\BackUp'

# Passo 6 - Gerar o nome do arquivo de backup com a data e hora atuais
now = datetime.now()
backup_file = f'{db_name}-{now.strftime("%Y-%m-%d_%H-%M-%S")}.sql'

# Passo 7 - Criar o comando para realizar o backup do banco de dados
backup_cmd = f'pg_dump -U {db_user} -W -F t -h {db_host} {db_name} -f {backup_path}{backup_file}'

# Passo 8 - Executar o comando de backup e armazenar a saída
output = subprocess.run(backup_cmd, shell=True, capture_output=True, text=True, env={'PGPASSWORD': db_password})

# Passo 9 - Verificar se o backup foi realizado com sucesso
if output.returncode == 0:
    print(f'Backup do banco de dados {db_name} realizado com sucesso em {backup_path}{backup_file}')

    # Passo 10 - Enviar o arquivo de backup por email
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_user
    msg['Subject'] = f'Backup do banco de dados {db_name} - {now.strftime("%Y-%m-%d %H:%M:%S")}'
    msg.attach(MIMEText('Backup do banco de dados foi realizado com sucesso e enviado por email'))

    part = MIMEApplication(open(f'{backup_path}{backup_file}', 'rb').read(), Name=backup_file)
    part['Content-Disposition'] = f'attachment; filename="{backup_file}"'
    msg.attach(part)

    smtp = smtplib.SM

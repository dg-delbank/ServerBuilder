import os
import subprocess
import time

print(' Default: ALL\n-------1.Portainer\n-------2.Nginx Proxy Manager\n-------3.Jenkins')
print('Para seleção manual digite o(s) valor(es) numério(s), separado(s) por vírgula(s).')

try:
    user_input = input('> ').strip()
    choice = [option.strip() for option in user_input.split(',') if option.strip()]
    if choice == []:
        choice = ['1', '2', '3']
except Exception as ex:
    print('Opção inválida.' + ex)

with open('ips.txt', 'w') as f:
    def verify_choice(choice):
        if '1' in choice:
            namePortainer = input('Digite o nome do container do Portainer (Default:portainer-delbank-hml-master): ') or 'portainer-delbank-hml-master'

            if namePortainer.strip() == 'prod':
                namePortainer = 'portainer-delbank-prod-master'

        if '2' in choice:
            nameNginx = input('Digite o nome do container do Nginx (Default:nginx-proxy-manager-delbank-hml-master): ') or 'nginx-proxy-manager-delbank-hml-master'

            if nameNginx.strip() == 'prod':
                nameNginx = 'nginx-proxy-manager-delbank-prod-master'

        if '3' in choice:
            nameJenkins = input('Digite o nome do container do Jenkins (Default:jenkins-delbank-hml-master): ') or 'jenkins-delbank-hml-master'

            if nameJenkins.strip() == 'prod':
                nameJenkins = 'jenkins-delbank-prod-master'

        if '1' in choice:
            os.system(f'docker volume create portainer_data')
            os.system(f'docker run -d -p 8000:8000 -p 9443:9443 --name {namePortainer} --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest')

            comando = ['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', namePortainer]
            ip = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True)
            f.write(f'{namePortainer}:{ip}\n')

            os.system('sudo ufw allow 9443')

        if '2' in choice:
            with open('docker-compose.yml', 'w') as docker_compose_file:
                docker_compose_file.write(f'''version: '3.8'
services:
  app:
    container_name: {nameNginx}
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - nginx_data:/data
      - nginx_letsencrypt:/etc/letsencrypt

volumes:
  nginx_data:
    name: nginx_data
  nginx_letsencrypt:
    name: nginx_letsencrypt
''')
            os.system('docker compose up -d')

            comando = ['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', nameNginx]
            ip = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True)
            f.write(f'{nameNginx}:{ip}\n')

            os.system('sudo ufw allow 80')
            os.system('sudo ufw allow 81')
            os.system('sudo ufw allow 443')
            os.system(f'sudo ufw allow from {ip}')

        if '3' in choice:
            os.system('docker volume create jenkins_data')
            os.system(f'docker run -d --restart always -u 1000:1000 -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_data:/var/jenkins_home --name {nameJenkins} jenkins/jenkins:latest')

            comando = ['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', nameJenkins]
            ip = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True)
            f.write(f'{nameJenkins}:{ip}\n')

            os.system('sudo ufw allow 8080')
            
            time.sleep(15)
            print('-----------Jenkins Admin Password:')
            os.system(f'docker exec {nameJenkins} cat /var/jenkins_home/secrets/initialAdminPassword')

        else:
            print('Opção não encontrada.')

    verify_choice(choice)

#print('Ativando Firewall...')
#daemon_json_content = '''
#{
# "iptables": false,
#  "dns": ["8.8.8.8", "8.8.4.4"]
#}
#'''
#try:
#    with open('/etc/docker/daemon.json', 'w') as file:
#        file.writelines(daemon_json_content)
    
#    os.system('sudo ufw default deny incoming')
#    os.system('yes | sudo ufw enable')
#    print('Firewall ativo.')

#except Exception as ex:
#    print('Erro ao criar daemon.json: ' + ex)

print('Fim do seja lá o que acabou de acontecer.')
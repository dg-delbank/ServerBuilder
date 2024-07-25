import os
import subprocess

print(' Default:\n-------1.Portainer\n-------2.Nginx Proxy Manager\n-------3.Jenkins')
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
            name = input('Digite o nome do container do Portainer: ') or 'portainer-delbank-hml-master'
            os.system(f'docker volume create portainer_data')
            os.system(f'docker run -d -p 8000:8000 -p 9443:9443 --name {name} --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest')

            comando = ['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', name]
            ip = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True)
            f.write(f'{name}:{ip}\n')

        if '2' in choice:
            name = input('Digite o nome do container do Nginx: ') or 'nginx-proxy-manager-delbank-hml-master'
            with open('docker-compose.yml', 'w') as docker_compose_file:
                docker_compose_file.write(f'''version: '3.8'
services:
  app:
    container_name: {name}
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
''')
            os.system('docker compose up -d')

            comando = ['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', name]
            ip = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True)
            f.write(f'{name}:{ip}\n')

        if '3' in choice:
            name = input('Digite o nome do container do Jenkins: ') or 'jenkins-delbank-hml-master'
            os.system(f'docker run -d -it --restart always -u root -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):/usr/bin/docker --name {name} jenkins/jenkins:latest')

            comando = ['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', name]
            ip = subprocess.check_output(comando, stderr=subprocess.STDOUT, text=True)
            f.write(f'{name}:{ip}\n')
            print('-----------Jenkins Admin Password:')
            os.system(f'docker exec {name} cat /var/jenkins_home/secrets/initialAdminPassword')

        else:
            print('Opção não encontrada.')

    verify_choice(choice)

print('Fim do seja lá o que acabou de acontecer.')
# Autor: Luan Santos
# Empresa: DNSecury - Desenvolvimento e Soluções em segurança cibernética.
# Descrição: Ferramento de scanner de infraestrutura, que tem como função mapear todos os dispositivos conectados a determinada rede.
# Versão: 0.1
# Licença: MIT Licence
#
# Contato: luanpsantos@outlook.com.br
#
# Ajuda:
#    # python exercício01.py --network 127.0.0.1/24

import os
import argparse
import threading

_help = """
python network_discovery.py [opção] [valor]

Opções:
    --network       Define a rede a ser mapeada.

Exemplo: 
        python network_discovery.py --network 127.0.0.1/24
"""

parse = argparse.ArgumentParser(description="Mapeamento de dispositivos de rede.")
parse.add_argument("--network", metavar="network", type=str, nargs='?')
args = parse.parse_args()


def network_discovery(ip, qnt_ips, flag, net):

    print(f"""
=============== Descoberta da rede {ip}/{str(net)} ===============
Pressione CTRL+C para sair.

            """)

    """ # Realiza o mapeamento da rede alterando apenas o ultimo octeto do endereço ip. """
    def scanner_one(ip, oct):
        return_command = os.popen(f"ping {str(ip[0])}.{str(ip[1])}.{str(ip[2])}.{str(oct)} -n 1").read()
        if "inacess¡vel" in return_command or "inacessível" in return_command or "Esgotado" in return_command:
            pass
        else:
            print(f"""[+] Descoberta: {str(ip[0])}.{str(ip[1])}.{str(ip[2])}.{str(oct)}""")

    """ # Realiza o mapeamento da rede alterando o penultimo e ultimo octeto do endereço ip. """
    def scanner_two(ip, oct, oct2):
        return_command = os.popen(f"ping {str(ip[0])}.{str(ip[1])}.{str(oct)}.{str(oct2)} -n 1").read()
        if "inacess¡vel" in return_command or "inacessível" in return_command or "Esgotado" in return_command:
            pass
        else:
            print(f"""[+] Descoberta: {str(ip[0])}.{str(ip[1])}.{str(oct)}.{str(oct2)}""")

    """ # Realiza o mapeamento da rede alterando o antepenúltimo, penultimo e ultimo octeto do endereço ip. """
    def scanner_three(ip, oct, oct2, oct3):
        return_command = os.popen(f"ping {str(ip[0])}.{str(oct)}.{str(oct2)}.{str(oct3)} -n 1").read()
        if "inacess¡vel" in return_command or "inacessível" in return_command or "Esgotado" in return_command:
            pass
        else:
            print(f"""[+] Descoberta: {str(ip[0])}.{str(oct)}.{str(oct2)}.{str(oct3)}""")

    """ # Dividindo o endereçamento informado como parâmetro. """
    ip = ip.split(".")

    """ # Montagem da rede /8. """
    if flag == 1:
        for oct in range(qnt_ips):
            for oct2 in range(qnt_ips):
                for oct3 in range(1, qnt_ips):
                    th = threading.Thread(target=scanner_three, args=(ip, oct, oct2, oct3))
                    th.start()

    elif flag == 2:
        """ # Montagem da rede /16. """
        for oct in range(qnt_ips):
            for oct2 in range(1, qnt_ips):
                th = threading.Thread(target=scanner_two, args=(ip, oct, oct2))
                th.start()

    elif flag == 3:
        """ # Montagem da rede /24. """
        for oct in range(1, qnt_ips):
            th = threading.Thread(target=scanner_one, args=(ip, oct))
            th.start()


""" # Tratamento de possíveis erros de parâmetros. """
if not args.network:
    print(_help)
    exit()

if "/" not in args.network or not args.network.split("/")[1]:
    print("Valor do argumento --network é inválido!")
    exit()

""" # Tratamento do tipo de rede a ser mapeada. """
if int(args.network.split("/")[1]) == 8:
    """ # Destinada a rede /8. """
    network_discovery(args.network.split("/")[0], 255, flag=1, net=8)

elif int(args.network.split("/")[1]) == 16:
    """ # Destinada a rede /16. """
    network_discovery(args.network.split("/")[0], 255, flag=2, net=16)

elif int(args.network.split("/")[1]) == 24:
    """ # Destinada a rede /24. """
    network_discovery(args.network.split("/")[0], 255, flag=3, net=24)

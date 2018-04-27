#!/usr/bin/python3
# buttcockles 1.0
import requests
import argparse
import socket
from lxml import html

def geddem(args):
    
    eh = "https://findsubdomains.com/subdomains-of/"
    dom = args.domain

    print("\033[1m[!] Looking up %s" % args.domain)
    p = requests.get(eh+dom.strip())
    
    print("\033[1m[!] Parsing shit...")

    blergh = html.fromstring(p.content)
    domains = blergh.find_class('row row-mobile')
    
    as_blocks = blergh.xpath('//td[@data-field="AS"]/text()')
    as_set = set(as_blocks)
    as_list = list(as_set)
    as_list.sort()

    print("\033[91m[+] Found "+str(len(domains))+" domains")
    print("\033[91m[+] Found "+str(len(as_list))+" AS")

    if args.o:
        ofile=open(args.o,"w")

    # as
    if args.a == True:
        for ass in as_list:
            if args.o:
                ofile.write(ass+"\n")
            else:
                print("\033[94m"+ass)

    rlist = []
    for goodie in domains:
        domain = goodie[0][1].text_content()
        ip = goodie[1][1].text_content()
        region = goodie[2][1].text_content()
        AS = goodie[3][1].text_content()
        org = goodie[4][1].text_content()

        # full output
        if args.f == True:
            if args.o:
                ofile.write("Domain: %s\nIP: %s\nRegion: %s\nAS: %s\nOrg: %s\n\n" % (domain, ip, region, AS, org))
            else:
                print("\033[92mDomain: %s\nIP: %s\nRegion: %s\nAS: %s\nOrg: %s\n" % (domain, ip, region, AS, org))

        # domains only
        if args.d == True:
            rlist.append(domain.strip())
        # ip
        if args.i == True:
            if not ip:
                try:
                    rlist.append(socket.gethostbyname(domain))
                except:
                    pass
            else:
                rlist.append(ip)


    rlist.sort()
    for res_elem in rlist:
        if args.o:
            ofile.write(res_elem+"\n")
        else:
            print("\033[92m"+res_elem)

    if args.o:
        print("\033[93mWrote results to: "+args.o)
            
        
if __name__ == "__main__":
    argps = argparse.ArgumentParser(prog="Buttcockles 1.0")
    argps.add_argument("domain")
    argps.add_argument("-f",action='store_true',help="full output")
    argps.add_argument("-i",action='store_true',help="output ip addresses")
    argps.add_argument("-d",action='store_true',help="output domains")
    argps.add_argument("-a",action='store_true',help="output AS")
    argps.add_argument("-o",help="output stuff to file")
    args = argps.parse_args()

    geddem(args)


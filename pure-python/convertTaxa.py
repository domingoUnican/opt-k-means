# -*- coding: utf-8 -*-
from argparse import ArgumentParser

n=0
cont=0
mylist=[]
coding={}
coding['a']=[3.0,-1.0,-1.0,-1.0]
coding['c']=[-1.0,3.0,-1.0,-1.0]
coding['g']=[-1.0,-1.0,3.0,-1.0]
coding['t']=[-1.0,-1.0,-1.0,3.0]
coding['u']=[-1.0,-1.0,-1.0,3.0]
coding['r']=[1-0,-1.0,1.0,-1.0]
coding['y']=[-1-0,1.0,-1.0,1.0]
coding['s']=[-1.0,1.0,1.0,-1.0]
coding['w']=[1.0,-1.0,-1.0,1.0]
coding['k']=[-1.0,-1.0,1.0,1.0]
coding['m']=[1.0,1.0,-1.0,-1.0]
coding['b']=[-1.0,1.0/3,1.0/3,1.0/3]
coding['d']=[1.0/3,-1.0,1.0/3,1.0/3]
coding['h']=[1.0/3,1.0/3,-1.0,1.0/3]
coding['v']=[1.0/3,1.0/3,1.0/3,-1.0]
coding['n']=[0.0,0.0,0.0,0.0]
coding['-']=[-1.0,-1.0,-1.0,-1.0]

if __name__=='__main__':
    parser = ArgumentParser(description='Convert nucleotide sequences into numerical data.')
    parser.add_argument('-i','--file_in', help='Input .fasta filename', required=True)
    parser.add_argument('-o','--file_out', help='Output .txt file', required=True)
    args = vars(parser.parse_args())    
    if args['file_in']:
        name_file_in = args['file_in']
    if args['file_out']:
        name_file_out = args['file_out']
    
    f_out=open(name_file_out,"w")
    with open(name_file_in) as f_in:
        for line in f_in:   
            n+=1
            if line[0]!='>':         
                for c in line[:-1]:
                    if c in 'acgturyswkmbdhvn-':
                        mylist.extend(coding[c])
                    else:
                       print "error",c,n
            else:
                cont+=1
                if len(mylist):
                    for w in mylist[:-1]:
                        f_out.write('%3.3f,'%w)
                    f_out.write('%3.3f\n'%mylist[-1])
                mylist=[]
    
    f_out.close()        
    f_log = open("data_log.txt","a")  
    f_log.write('Fichero ' + name_file_out + '\t Filas ' + str(cont) + '\n')
    f_log.close()

        
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 20:10:40 2017

@author: dell_zejunzh
"""
import time
import copy
from graphviz import Digraph

class Rule(object):
    def __init__(self,left,right):
        self.left_str=left
        self.right_str=right
class active_edge(object):
    def __init__(self,start_pos,end_pos,gnera_l,gnera_r,ac_pos=0):
        self.start_pos=start_pos
        self.end_pos=end_pos
        self.gnera_l=gnera_l
        self.gnera_r=gnera_r
        self.ac_pos=ac_pos
    def get_parms(self):
        return self.start_pos,self.end_pos,self.gnera_l,self.gnera_r,self.ac_pos
class un_active_edge(object):
    def __init__(self,start_pos,end_pos,rule_str):
        self.start_pos=start_pos
        self.end_pos=end_pos
        self.rule_str=rule_str
    def get_parms(self):
        return self.start_pos,self.end_pos,self.rule_str
class agenda(object):
    def __init__(self,start_pos,end_pos,rule_str):
        self.start_pos=start_pos
        self.end_pos=end_pos
        self.rule_str=rule_str
    def get_parms(self):
        return self.start_pos,self.end_pos,self.rule_str
def pre_process(iput_string,iput_rule_str,Rules_list,dot):
    dot.node_attr.update(color='lightblue2', style='filled')
    dot.attr(size='7,3',rankdir="LR",rank="same")
    f_sentence=open("sentence.txt",'r')
    for line in f_sentence:
        for i in range(len(line.split())):
            iput_string.append(line.split()[i])
    f_cixng=open("cixing.txt",'r')
    count=0
    for line in f_cixng:
        line_fuzhu=line.split() ;
        for i,cixing in enumerate(line_fuzhu):
            count=count+1
            iput_rule_str.append([cixing,count,count+1])
#    print(iput_string,iput_rule_str)

    f_rules=open("rules.txt",'r')
    for line in f_rules:
        line_fuzhu=line.split() ;
        rule=Rule(line_fuzhu[0],line_fuzhu[1:])
        Rules_list.append(rule)
    return 0
def chart_parse(iput_rule_str,Agenda,Rules_list,Un_Active_edge,Active_edge):
    data=copy.copy(iput_rule_str)
    len_agenda=len(Agenda)
    count=0
    while(len(Agenda)>0 or len(data)>0):
        count=count+1
#        print count
        len_agenda=len(Agenda)
        if len_agenda==0:
            Agenda.append(agenda(data[0][1],data[0][2],data[0][0]))
            data.remove(data[0])
        c_agenda=Agenda.pop()
#        print "len:",len(Agenda),c_agenda. get_parms(),data[0]
        #add_active-edge()
#        for 
        for i,rule in enumerate(Rules_list):
            if rule.right_str[0]==c_agenda.rule_str:
                if len(rule.right_str)==1:
                    Agenda.append(agenda(c_agenda.start_pos,c_agenda.end_pos,rule.left_str))
                else:
                    Active_edge.append(active_edge(c_agenda.start_pos,c_agenda.end_pos,rule.left_str,rule.right_str,1))
#                    print (i,active_edge(c_agenda.start_pos,c_agenda.end_pos,rule.left_str,rule.right_str,1).get_parms())
        Un_Active_edge.append(un_active_edge(c_agenda.start_pos,c_agenda.end_pos,c_agenda.rule_str))
        #add_Un_active-edge()
        for i,act_edge in enumerate(Active_edge):
            if act_edge.gnera_r[act_edge.ac_pos]==c_agenda.rule_str and act_edge.end_pos==c_agenda.start_pos :
#                print "test:",act_edge.gnera_r
                if act_edge.ac_pos+1==len(act_edge.gnera_r):
                    Agenda.append(agenda(act_edge.start_pos,c_agenda.end_pos,act_edge.gnera_l))
                else:
                    Active_edge.append(active_edge(act_edge.start_pos,c_agenda.end_pos,act_edge.gnera_l,act_edge.gnera_r,act_edge.ac_pos+1))
            
    return 0;

def print_information(Un_Active_edge,Active_edge,dot,iput_string):
    f_result=open("results.txt",'w')
    if Un_Active_edge[len(Un_Active_edge)-1].start_pos==1 and  Un_Active_edge[len(Un_Active_edge)-1].end_pos==len(iput_rule_str)+1 and  Un_Active_edge[len(Un_Active_edge)-1].rule_str:
        print ("{} 符合句法\n".format(' '.join(map(str, iput_string))))
        f_result.write("{} 符合句法\n".format(' '.join(map(str, iput_string))))
    else:
        print("{} 不符合chartparsing句法\n".format(' '.join(map(str, iput_string))))
        f_result.write("{} 不符合chartparsing句法\n".format(' '.join(map(str, iput_string))))
    print("非活动边：\n")
    f_result.write("非活动边：\n")
    for i,un_act_edge in enumerate(Un_Active_edge):
        dot.attr('edge',style='filled')
        dot.edge(str(un_act_edge.start_pos),str(un_act_edge.end_pos),label=un_act_edge.rule_str)
        print (un_act_edge.get_parms())
        f_result.write( (' '.join(map(str, un_act_edge.get_parms())))+"\n")
#        f_result.write(un_act_edge.get_parms())
    print("活动边：\n")
    f_result.write("活动边：\n")
    for i,act_edge in enumerate(Active_edge):
        dot.attr('edge',style='dotted')
        dot.edge(str(act_edge.start_pos),str(act_edge.end_pos),label="{} -> {}".format(
            act_edge.gnera_l,
            ' '.join(map(str, act_edge.gnera_r))))
        print ("%s %s %s->%s %d\n" %(act_edge.start_pos,act_edge.end_pos,act_edge.gnera_l,(' '.join(map(str, act_edge.gnera_r))),act_edge.ac_pos))
        f_result.write( "%s %s %s->%s %d\n" %(act_edge.start_pos,act_edge.end_pos,act_edge.gnera_l,(' '.join(map(str, act_edge.gnera_r))),act_edge.ac_pos))
#        f_result.write(act_edge.get_parms())
    dot.render('chart-parsing.gv', view=True) 
    return 0
if __name__=="__main__":
    dot = Digraph(comment='The chart parsing')
    Rules_list=[]
    Agenda=[]
    Active_edge=[]
    Un_Active_edge=[]
    iput_string=[]
    iput_rule_str=[]
    pre_process(iput_string,iput_rule_str,Rules_list,dot)
    chart_parse(iput_rule_str,Agenda,Rules_list,Un_Active_edge,Active_edge)
    print_information(Un_Active_edge,Active_edge,dot,iput_string)
    time.sleep(5)


import sys

def main():
	runParsed = Parser(Scanner().scanFile(sys.argv[1]) , 0).runParse()
	StackMachine(runParsed["symtable"], runParsed["dNodes"]).StackMach()

class Scanner(object):
    def __init__(self):
        self.modeStr = False
        self.recStr = ""
        self.row = 1
        self.col = 1
        self.tk = ""
        self.comment = False
        self.numeric = False
        self.real = False
        self.tokenArr = []
        self.tableArr = []

    def display(self):
        print " %30s %20s %20s " % ( "Token", "Value", "Line", )
        for tkn in self.tokenArr:
            tok = str(tkn[0])
            val = str(tkn[1])
            lin = str(tkn[2])
            print "%30s %20s %20s " % ( tok, val, lin,)

    def stringProcess(self, inputChar):
        if ord(inputChar) == 39:
            self.recStr += inputChar
            self.tokenArr.append(("strTok", self.recStr, self.row, self.col))
            self.tableArr.append({"TOKEN" : "strTok", "Val" : self.recStr, "ROW" : self.row, "COL" : self.col})
            self.recStr = ""
            self.modeStr = False
            return
        else:
            self.recStr += inputChar

    def numberProcess(self, inputChar):
	
        if inputChar.isdigit():
            self.recStr += inputChar

        if ord(inputChar) > 57 or ord(inputChar) <= 41:
            self.numeric = False
            if self.real:
                self.tokenArr.append(("realToken", self.recStr, self.row, self.col-1))
                self.tableArr.append({"TOKEN" : "realToken", "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
                self.real = False
            else:
                self.tokenArr.append(( "intTok", self.recStr, self.row, self.col-1))
                self.tableArr.append({"TOKEN" : "intTok", "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})

            if inputChar in self.Dictionary:
                if self.tk:
                    self.tk =""
                self.tokenArr.append(( self.Dictionary[inputChar], inputChar, self.row, self.col))
                self.tableArr.append({"TOKEN" : self.Dictionary[inputChar], "Val" : inputChar, "ROW" : self.row, "COL" : self.col})

            self.recStr = ""
            return

        if ord(inputChar) == 46:
            self.real = True
            self.recStr += inputChar
            return

    def stateProcess(self, inputChar):
        if ord(inputChar) <= 32:         
            if self.tk:
                if self.changeCase(self.recStr) in self.Dictionary:
                    self.tokenArr.append((self.Dictionary[self.changeCase(self.recStr)], self.recStr, self.row, self.col-1))
                    self.tableArr.append({"TOKEN" : self.Dictionary[self.changeCase(self.recStr)], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
                    self.tk =""
                    self.recStr = ""
                    return
                if self.changeCase(self.recStr) not in self.Dictionary:
                    self.tokenArr.append((self.Dictionary[self.tk], self.recStr, self.row, self.col-1))
                    self.tableArr.append({"TOKEN" : self.Dictionary[self.tk], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
                    self.tk =""
                    self.recStr = ""
                    return                    

            if not self.tk:
                return        

        if ord(inputChar) == 39:
            self.recStr =""
            self.modeStr = True
            self.recStr += inputChar
            return

        if inputChar.isdigit() :
            self.numeric = True
            self.recStr += inputChar
            return

        if ord(inputChar)==46:
            if self.tk:
                self.recStr +=inputChar 
                self.tokenArr.append((self.Dictionary[self.changeCase(self.recStr)], self.recStr, self.row, self.col))
                self.tableArr.append({"TOKEN" : self.Dictionary[self.changeCase(self.recStr)], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col})
                self.recStr = ""
                self.tk=""
                return

        if ord(inputChar) == 59 and not self.numeric:
            if not self.tk:
                if self.recStr:
                    self.tokenArr.append((self.Dictionary["IDENTIFIER"], self.recStr, self.row, self.col-1))
                    self.tableArr.append({"TOKEN" : self.Dictionary["IDENTIFIER"], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
            else:
                if self.changeCase(self.recStr) == "END":
                    self.recStr +=inputChar
                    self.tokenArr.append((self.Dictionary[self.changeCase(self.recStr)], self.recStr, self.row, self.col-1))
                    self.tableArr.append({"TOKEN" : self.Dictionary[self.changeCase(self.recStr)], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
                else:
                    self.tokenArr.append((self.Dictionary[self.changeCase(self.tk)], self.recStr, self.row, self.col-1))
                    self.tableArr.append({"TOKEN" : self.Dictionary[self.changeCase(self.tk)], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
            if self.changeCase(self.recStr) != "END;":
                self.tokenArr.append((self.Dictionary[inputChar],inputChar, self.row, self.col))
                self.tableArr.append({"TOKEN" : self.Dictionary[inputChar], "Val" : inputChar, "ROW" : self.row, "COL" : self.col})
            self.recStr = ""
            self.tk =""
            return

        if ord(inputChar) == 58:
            if self.recStr:
                self.tokenArr.append((self.Dictionary["IDENTIFIER"], self.recStr, self.row, self.col-2))
                self.tableArr.append({"TOKEN" : self.Dictionary["IDENTIFIER"], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-2})          
            self.recStr = inputChar
            self.tk = inputChar
            return

        if ord(inputChar) == 61:
            if not self.tk:
                if self.recStr != "":
                    self.tokenArr.append((self.Dictionary["IDENTIFIER"], self.recStr, self.row, self.col))
                    self.tableArr.append({"TOKEN" : self.Dictionary["IDENTIFIER"], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col})
                self.tokenArr.append((self.Dictionary["="], "=", self.row, self.col))
                self.tableArr.append({"TOKEN" : self.Dictionary["="], "Val" : "=", "ROW" : self.row, "COL" : self.col})
                self.recStr = ""
                return                
            if self.tk:
                self.recStr +=inputChar
                if self.recStr in self.Dictionary:
                    self.tokenArr.append((self.Dictionary[self.recStr], self.recStr, self.row, self.col))
                    self.tableArr.append({"TOKEN" : self.Dictionary[self.recStr], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col})
                    self.recStr = ""
                    self.tk = ""
                    return

        if ord(inputChar) == 43 or ord(inputChar) == 45:
            self.tokenArr.append((self.Dictionary[inputChar], inputChar, self.row, self.col-1))
            self.tableArr.append({"TOKEN" : self.Dictionary[inputChar], "Val" : inputChar, "ROW" : self.row, "COL" : self.col-1})
            self.recStr = ""
            return

        if ord(inputChar) == 40:
            if self.recStr:
                self.tokenArr.append((self.Dictionary[self.changeCase(self.recStr)], self.recStr, self.row, self.col-1))
                self.tableArr.append({"TOKEN" : self.Dictionary[self.changeCase(self.recStr)], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
                self.tokenArr.append((self.Dictionary[inputChar],inputChar, self.row, self.col))
                self.tableArr.append({"TOKEN" : self.Dictionary[inputChar], "Val" : inputChar, "ROW" : self.row, "COL" : self.col})
                self.recStr = ""
                self.tk = inputChar
                return
                
        if ord(inputChar) == 41:
            if self.tk:
                if self.recStr:
                    self.tokenArr.append((self.Dictionary["IDENTIFIER"], self.recStr, self.row, self.col-1))
                    self.tableArr.append({"TOKEN" : self.Dictionary["IDENTIFIER"], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
                self.tokenArr.append((self.Dictionary[inputChar], inputChar, self.row, self.col))
                self.tableArr.append({"TOKEN" : self.Dictionary[inputChar], "Val" : inputChar, "ROW" : self.row, "COL" : self.col})
            self.recStr = ""
            self.tk  = ""
            return

        if ord(inputChar) == 42:
            if self.tk:
                self.comment = True
                self.recStr += inputChar
                return

        if ord(inputChar) == 44:
            if self.recStr:
                self.tokenArr.append((self.Dictionary["IDENTIFIER"], self.recStr, self.row, self.col-1))
                self.tableArr.append({"TOKEN" : self.Dictionary["IDENTIFIER"], "Val" : self.recStr, "ROW" : self.row, "COL" : self.col-1})
                self.tokenArr.append((self.Dictionary[inputChar], inputChar, self.row, self.col))
                self.tableArr.append({"TOKEN" : self.Dictionary[inputChar], "Val" : inputChar, "ROW" : self.row, "COL" : self.col})
                self.recStr = ""
                self.tk = ""
                return

        if ord(inputChar) == 60 or ord(inputChar) == 62:
            self.recStr = inputChar
            self.tk = inputChar
            return

        self.recStr += inputChar

        if self.changeCase(self.recStr) != "END":
            if self.changeCase(self.recStr) not in self.Dictionary:
                self.tk = "IDENTIFIER"
                return
            if self.changeCase(self.recStr) in self.Dictionary:
                self.tk = self.recStr
                return

    def commentProcess(self,inputChar):
        if ord(inputChar) == 41:
            if self.tk:
                self.recStr += inputChar
                self.tokenArr.append(("commTok", self.recStr, self.row, self.col))
                self.tableArr.append({"TOKEN" : "commTok", "Val" : self.recStr, "ROW" : self.row, "COL" : self.col})                
                self.comment = False
                self.tk =""
                self.recStr = ""
                return
        else:
            self.recStr += inputChar

    def scanFile(self, input):
        output = open(input, "r").readlines()
        for line in output:
            for inputChar in line:
                if self.comment:
                    self.commentProcess(inputChar)
                    if ord(inputChar) == 10:
                        self.col = 0
                        self.row += 1
                elif self.modeStr:
                    self.stringProcess(inputChar)
                    if ord(inputChar) == 10:
                        self.col = 0
                        self.row += 1
                elif self.numeric:
                    self.numberProcess(inputChar)                 
                    if ord(inputChar) == 10:
                        self.col = 0
                        self.row += 1
                else:
                    self.stateProcess(inputChar)
                    if ord(inputChar) == 10: 
                        self.col = 0
                        self.row += 1               
                self.col += 1
        self.display()
        return self.tokenArr

    def changeCase(self, inputChar):
        return inputChar.upper()

    Dictionary = {
        "BEGIN" : "beginToken", "END." : "endDotToken", "," : "commaToken", "INTEGER" : "idIntToken", "BOOLEAN" : "idBoolToken", "+" : "addToken", "-" : "minusToken", "*" : "multsteplyToken",
        "STRING" : "stringToken", "CHAR" : "charToken", "REAL" : "realToken",  "FLOAT" : "floatToken", "PROGRAM" : "progToken", "WRITELN" : "writeLineToken", "READLN" : "readLineToken",
        "USES" : "useToken", "VAR" : "variableToken", "IDENTIFIER": "idenToken", "CASE" : "caseToken", "OF" : "ofToken", "REPEAT" : "repeatToken", "OR" : "orToken", "NOT" : "notToken",		
		"=" : "equalToToken", "<" : "lessThanToken", ">" : "greaterThanToken", "<=" : "lessOrEqualToken", ">=" : "greaterOrEqualToken", "DIV" : "divFloatToken", "MOD" : "modToken", "AND" : "andToken", 
        "IF" : "ifToken", "THEN" : "thenToken", "ELSE" : "elseToken", "FOR" : "forToken", "TO" : "toToken", "DO" : "doToken", "/" : "divToken", ";" : "semicolonToken", ":" : "colonToken",  
        "END;" : "endToken", "UNTIL" : "untilToken", "WHILE" : "whileToken", ":=" : "assignToken", "(" : "leftParenToken", ")" : "rightParenToken",
    }          
    
class Parser(object):
    def __init__(self, tokList, tk):
        self.tokList = tokList
        self.tk = tk
        self.itera = self.createIter()
        self.dNodes = []
        self.nodes = []
        self.tableSym = []
        self.step = 0
        self.op = False
        self.addr = 0
        self.leftHandSide = ""
        self.rightHandSide = ""
        self.tmp = False
        self.switchOn = False
        self.hSwitch = 0

    def retrieve(self):
        self.tokenRetreive()
        self.matchAndAppend()

    def runParse(self):
        self.retrieve()
        self.display()
        return {"symtable": self.tableSym, "dNodes": self.dNodes}

    def display(self):
        print ""
        print "Instructions Table"
        print " %15s %10s " %("Instruction", "Val")
        for tkn in self.dNodes:
            print "%15s %10s " %( str(tkn["instruction"]), str(tkn["val"]))
        print ""
        print "Symbols Table"
        print " %8s %8s %10s %10s " %("Token", "Val", "Type", "Addr")
        for tkn in self.tableSym:
			print "%8s %8s %10s %10s " %( str(tkn["Name"]), str(tkn["Val"]), str(tkn["Type"]), tkn["Addr"])

    def createIter(self):
        tokenArr = iter(self.tokList)
        return tokenArr

    def tokenRetreive(self):
        self.tk = self.itera.next()

    def declars(self):
        self.initialVars()

    def wrongToken(self, tkn):
        print "Wrong token"

    def matchAndAppend(self):
        if self.tk[0] == "progToken":
            self.findMatching("progToken")
            self.declars()
            self.tokenMatchingBeg()
            if self.tk[0] == "endToken":
                self.findMatching("endToken")
                if self.tk[0] == "endDotToken":
                    self.dNodes.append({"instruction": "done", "step": self.step, "val": self.tk[1]})
            else:
                self.dNodes.append({"instruction": "done", "step": self.step, "val": self.tk[1]})

    def initialVars(self):
        if self.tk[0] == "variableToken":
            self.findMatching("variableToken")
        else:
            self.tokenMatchingBeg()
            return

        while (1):
            if self.tk[0] == "idenToken":
                self.tableSym.append({"Name": self.tk[1], "Addr": self.addr, "Type": "none", "Val": 0})
                self.findMatching("idenToken")
                self.addr += 4
            elif self.tk[0] == "commaToken":
                self.findMatching("commaToken")
            elif self.tk[0] == "colonToken":
                self.findMatching("colonToken")
                break

        if self.tk[0] == "idIntToken":
            for sym in self.tableSym:
                if sym["Type"] == "none":
                    sym["Type"] = "int"
            self.findMatching("idIntToken")

        if self.tk[0] == "stringToken":
            for sym in self.tableSym:
                if sym["Type"] == "none":
                    sym["Type"] = "str"
            self.findMatching("stringToken")

        if self.tk[0] == "charToken":
            for sym in self.tableSym:
                if sym["Type"] == "none":
                    sym["Type"] = "char"
            self.findMatching("charToken")

        if self.tk[0] == "semicolonToken":
            self.findMatching("semicolonToken")

        self.initialVars()

    def exprn(self):
        self.trm()
        self.primeExprn()

    def tokenMatchingBeg(self):
        if self.tk[0] == "beginToken":
            self.findMatching("beginToken")
        self.tokenMatching()

    def tokenMatching(self):
        while(1):        
            if self.tk[0] == "idenToken":
                self.leftHandSide = self.tk
                self.findMatching("idenToken")
                self.exprn()

            if self.tk[0] == "forToken":
                self.Forloop()

            if self.tk[0] == "caseToken":
                self.switchStatement()

            if self.tk[0] == "repeatToken":
                self.Repeatloop()

            if self.tk[0] == "whileToken":
                self.whileloop()
            
            if self.tk[0] == "writeLineToken":
                self.keywordWrite()    

            if self.tk[0] == "ifToken":
                self.ifstatement()

            if self.tk[0] =="assignToken":
                self.findMatching("assignToken")
                self.exprn()
                self.op = True

            if self.tk[0] == "semicolonToken":
                self.findMatching("semicolonToken")
                if self.op:
                    self.dNodes.append({"instruction": "pop", "val":self.leftHandSide[1], "step": self.step})
                    self.step += 1
                    self.op = False
                if self.switchOn:
                    break
                else:
                    self.initialVars()
            
            if self.tk[0] == "untilToken" or self.tk[0] == "toToken":
                return

            if self.tk[0] == "elseToken":
                return

            if self.tk[0] == "endDotToken" or self.tk[0] == "endToken":
                break

    def comparSigns(self):
        if self.tk[0] == "equalToToken":
            self.findMatching("equalToToken")
            self.exprn()
            self.afterModify("equalToToken")
        elif self.tk[0] == "greaterThanToken":
            self.findMatching("greaterThanToken")
            self.exprn()
            self.afterModify("greaterThanToken")
        elif self.tk[0] == "lessOrEqualToken":
            self.findMatching("lessOrEqualToken")
            self.exprn()
            self.afterModify("lessOrEqualToken")
        elif self.tk[0] == "greaterOrEqualToken":
            self.findMatching("greaterOrEqualToken")
            self.exprn()
            self.afterModify("greaterOrEqualToken")
        else:
            self.exprn()

    def switchStatement(self):
        self.switchOn = True
        self.findMatching("caseToken")
        self.findMatching("leftParenToken")
        target = self.tk
        self.exprn()
        self.findMatching("rightParenToken")
        self.findMatching("ofToken")    
        self.runParseStatement(target)
        self.tokenMatching()

    def runParseStatement(self, target):
        print "runParseStatement"
        while(1):
            print str(target) + "  " + str(self.tk)
            self.hSwitch = self.step
            print "switchhole "+ str(self.hSwitch)
            self.labelParse(target)
            if self.tk[0] == "endToken":
                self.findMatching("endToken")
                break
        
        for sym in self.dNodes:
            if sym["instruction"] == "jump":
                if sym["val"] == 0:
                    sym["val"] = self.step

    def labelParse(self, target):
        print "self.step" + str(self.step)
        if self.tk[0] == "strTok":
            if not self.tmp:
                self.dNodes.append({"instruction":"push", "val":self.tk[1], "type": self.tk[0], "step": self.step})
                self.step += 1
                self.tmp = True
            else:
                self.dNodes.append({"instruction":"push", "val":target[1], "type": target[0], "step": self.step})
                self.step += 1                
                self.dNodes.append({"instruction":"push", "val":self.tk[1], "type": self.tk[0], "step": self.step})
                self.step += 1        
            self.dNodes.append({"instruction": "equals", "val":"equals", "type": self.tk[0], "step": self.step}) 
            self.step += 1
            self.dNodes.append({"instruction": "yesJmp", "val": self.step+2, "step": self.step})
            self.step +=1
            self.dNodes.append({"instruction": "jump", "val": self.step+4, "step": self.step})
            self.step +=1                            
            self.findMatching("strTok")            
        elif self.tk[0] == "commaToken":
            self.findMatching("commaToken")
            self.dNodes[self.step-1]["val"] =self.step            
        elif self.tk[0] == "colonToken":
            self.findMatching("colonToken")
            self.tokenMatching()
            self.dNodes.append({"instruction": "jump", "val": 0, "step": self.step})
            self.step +=1

    def trm(self):
        self.factKeyword()
        self.primeTrm()
		
    def ifstatement(self):
        self.findMatching("ifToken")
        self.findMatching("leftParenToken")
        self.exprn()
        self.comparSigns()
        self.findMatching("rightParenToken")
        self.findMatching ("thenToken")
        hole1 = self.step
        self.dNodes.append({"instruction": "notJmp", "step": self.step, "val": self.step})
        self.step += 1
        self.tokenMatching()

        if self.tk[0] == "elseToken":
            self.findMatching("elseToken")
            hole2 = self.step 
            self.dNodes.append({"instruction": "jump", "step": self.step, "val": 0})
            self.step += 1
            self.dNodes[hole1]["val"] = self.step
            self.tokenMatching()
            self.dNodes[hole2]["val"] = self.step
        
    def Forloop(self):
        self.findMatching("forToken")
        for sym in self.tableSym:
            if self.tk[1] == sym["Name"]:
                loop_variable =  self.tk
                break
        self.findMatching("idenToken")
        self.findMatching("assignToken")
        self.dNodes.append({"instruction": "push", "val": self.tk[1], "type": self.tk[0], "step": self.step})
        self.step += 1        
        self.dNodes.append({"instruction": "pop", "val":loop_variable[1], "type": loop_variable[0], "step": self.step})
        self.step += 1
        target = self.step
        self.dNodes.append({"instruction": "push", "val":loop_variable[1], "type": loop_variable[0], "step": self.step})
        self.step += 1
        self.findMatching("intTok")
        self.findMatching("toToken")
        self.dNodes.append({"instruction": "push", "val":self.tk[1], "type": self.tk[0], "step": self.step})
        self.step += 1
        self.findMatching("intTok")
        self.findMatching("doToken")
        self.dNodes.append({"instruction": "greater", "val":"greater","type": loop_variable[0], "step":self.step})
        self.step += 1
        hole = self.step
        self.dNodes.append({"instruction": "yesJmp", "val":self.step, "step":hole})
        self.step +=1
        self.findMatching("beginToken")
        self.tokenMatching()
        self.dNodes.append({"instruction": "push","val": loop_variable[1], "type" :loop_variable[0], "step":self.step})
        self.step += 1
        self.dNodes.append({"instruction": "push","val": 1, "type": "intTok", "step":self.step})
        self.step += 1
        self.dNodes.append({"instruction": "add","val":"+", "step": self.step})
        self.step += 1
        self.dNodes.append({"instruction": "pop", "val": loop_variable[1], "type": loop_variable[0], "step":self.step})
        self.step += 1
        self.dNodes.append({"instruction": "jump", "val": target, "step": self.step})
        self.step += 1
        self.dNodes[hole]["val"] = self.step

    def Repeatloop(self):
        target = self.step
        self.findMatching("repeatToken")
        self.tokenMatching()
        self.findMatching("untilToken")
        self.exprn()
        self.comparSigns()
        self.dNodes.append({"instruction": "notJmp", "step": self.step, "val": target })
        self.step +=1

    def findMatching(self, tkn):
        if (self.tk[0] == tkn):
            if (self.tk[1] == ")" or self.tk[1] == "("):
                pass
            else:
                self.nodes.append(self.tk[1])
            self.tokenRetreive()
            return True

    def whileloop(self):
        self.findMatching("whileToken")
        target = self.step    
        self.comparSigns()
        self.findMatching("doToken")
        self.dNodes.append({"instruction": "notJmp", "step": self.step, "val": target})
        hole = self.step
        self.step += 1
        self.tokenMatchingBeg()
        self.dNodes.append({"instruction": "jump", "step":self.step, "val": target})
        self.step += 1
        self.dNodes[hole]["val"] = self.step

    def afterModify(self, tkn):
        if tkn == "addToken":
            self.dNodes.append({"instruction": "add","val":"+", "type" :tkn, "step": self.step})
        elif tkn == "minusToken":
            self.dNodes.append({"instruction": "subtract","val":"-", "type" :tkn, "step": self.step})
        elif tkn == "multsteplyToken":
            self.dNodes.append({"instruction": "multiply","val":"*", "type" :tkn, "step":self.step})
        elif tkn == "divToken":
            self.dNodes.append({"instruction": "divide","val":"/", "type" :tkn, "step":self.step})
        elif tkn == "modToken":
            self.dNodes.append({"instruction": "modulus","val":"modulus", "type" :tkn, "step":self.step})
        elif tkn == "equalToToken":
            self.dNodes.append({"instruction": "equals", "val":"equals", "type": tkn, "step":self.step})
        elif tkn == "lessThanToken":
            self.dNodes.append({"instruction": "less", "val": "less", "type": tkn, "step":self.step})
        elif tkn == "greaterThanToken":
            self.dNodes.append({"instruction": "greater", "val": "greater", "type": tkn, "step":self.step})
        elif tkn == "greaterOrEqualToken":
            self.dNodes.append({"instruction": "gtr_equal", "val": "gtr_equal", "type": tkn, "step":self.step})
        elif tkn == "lessOrEqualToken":
            self.dNodes.append({"instruction": "lss_equal", "val": "lss_eq", "type": tkn, "step":self.step})
        elif tkn[0] == "idenToken":
            self.dNodes.append({"instruction": "push","val":self.tk[1], "type" :self.tk[0], "step":self.step})
        elif tkn[0] == "strTok":
            self.dNodes.append({"instruction": "push", "val":self.tk[1], "type":self.tk[0], "step": self.step})
        elif tkn[0] == "intTok":
            self.dNodes.append({"instruction": "push","val":self.tk[1], "type" :self.tk[0], "step":self.step})        
        elif tkn == "writeLineToken":
            self.dNodes.append({"instruction": "lineWrite", "val": "lineWrite" ,"type": tkn, "step":self.step})
        else:
            pass
        self.step +=1    

    def keywordWrite(self):
        if self.tk[0] == "writeLineToken":
            self.findMatching("writeLineToken")
            self.findMatching("leftParenToken")
            self.exprn()
            self.findMatching("rightParenToken")
            self.afterModify("writeLineToken")

    def primeExprn(self):
        if self.tk[0] == "addToken":
            self.findMatching("addToken")
            self.trm()
            self.afterModify("addToken")            
            self.primeExprn()
        elif self.tk[0] == "minusToken":
            self.findMatching("minusToken")
            self.trm()
            self.afterModify("minusToken")
            self.primeExprn()
        else:
            pass

    def primeTrm(self):
        if self.tk[0] == "multsteplyToken":
            self.findMatching("multsteplyToken")
            self.factKeyword()
            self.afterModify("multsteplyToken")
            self.primeTrm()
        elif self.tk[0] == "divToken":
            self.findMatching("divToken")
            self.factKeyword()
            self.afterModify("divToken")
            self.primeTrm()
        elif self.tk[0] == "modToken":
            self.findMatching("modToken")
            self.factKeyword()
            self.afterModify("modToken")
            self.primeTrm()
        elif self.tk[0] == "equalToToken":
            self.findMatching("equalToToken")
            self.exprn()
            self.afterModify("equalToToken")
        elif self.tk[0] == "lessThanToken":
            self.findMatching("lessThanToken")
            self.exprn()
            self.afterModify("lessThanToken")
        else:
            pass

    def factKeyword(self):
        if self.tk[0] == "idenToken":
            self.afterModify(self.tk)
            self.findMatching("idenToken")
            return

        if self.tk[0] == "strTok":
            self.afterModify(self.tk)
            self.findMatching("strTok")
            return

        if self.tk[0] == "intTok":
            self.afterModify(self.tk)
            self.findMatching("intTok")
            return

        if self.tk[0] == "notToken":
            self.findMatching("notToken")
            self.factKeyword()
            self.afterModify(self.tk)
            self.dNodes.append({"instruction": "not", "val":"not", "type":"notToken"})
            return
  
class StackMachine(object):
    def __init__(self, symtable, dNodes):
        self.symtable = symtable
        self.dNodes = dNodes
        self.stack = []
        self.step = 0

    def done(self):
        self.display()
        sys.exit(0)

    def jump(self, val):
        self.step = val - 1

    def notJmp(self, val):
        val1 = self.stack.pop()
        if val1 == False:
            self.step = val - 1

    def yesJmp(self, val):
        val1 = self.stack.pop()
        if val1 == True:
            self.step = val -1

    def lineWrite(self):
        val1 = self.stack.pop()

    def display(self):
        print "########Computing the Pascal Code and Outputing the Value#########"
        print " %8s %8s %10s %10s " %("Token", "Val", "Type", "Addr")
        for tkn in self.symtable:
            print "%8s %8s %10s %10s " %( str(tkn["Name"]), str(tkn["Val"]), str(tkn["Type"]), tkn["Addr"])


    def pop(self, val):
        val1 = self.stack.pop()
        for sym in self.symtable:
            if val == sym["Name"]:
                sym["Val"] = val1
        print "Symbol Table: " + str(self.symtable)

    def push(self, val):
        self.stack.insert(0, val)
        print "Symbol Table: " + str(self.symtable)
    def valPush(self, val):
        for sym in self.symtable:
            if val == sym["Name"]:
                self.stack.insert(0, sym["Val"])
        print "Symbol Table: " + str(self.symtable)

    def add(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = int(val1) + int(val2)
        self.push(tkn)
    def multiply(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = int(val1) * int(val2)
        self.push(tkn)

    def divide(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = int(val1) / int(val2)
        self.push(tkn)

    def subtract(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = int(val1) - int(val2)
        self.push(tkn)

    def modulus(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = int(val1) % int(val2)
        self.push(tkn)

    def StackMach(self):
        print ""
        print "         Stack Machine           "

        while(1):
            print ""
            print "Step Processing: " + str(self.dNodes[self.step]["instruction"]) + " " + str(self.dNodes[self.step]["val"])
            if self.dNodes[self.step]["instruction"] == "push":
                if self.dNodes[self.step]["type"] == "idenToken":
                    self.valPush(self.dNodes[self.step]["val"])
                else:
                    self.push(self.dNodes[self.step]["val"])
            elif self.dNodes[self.step]["instruction"] == "pop":
                self.pop(self.dNodes[self.step]["val"])
            elif self.dNodes[self.step]["instruction"] == "add":
                self.add()
            elif self.dNodes[self.step]["instruction"] == "subtract":
                self.subtract()
            elif self.dNodes[self.step]["instruction"] == "multiply":
                self.multiply()
            elif self.dNodes[self.step]["instruction"] == "divide":
                self.divide()
            elif self.dNodes[self.step]["instruction"] == "less":
                self.less()
            elif self.dNodes[self.step]["instruction"] == "greater":
                self.greater()
            elif self.dNodes[self.step]["instruction"] == "equals":
                self.equals()
            elif self.dNodes[self.step]["instruction"] == "modulus":
                self.modulus()
            elif self.dNodes[self.step]["instruction"] == "done":
                self.done()
            elif self.dNodes[self.step]["instruction"] == "jump":
                self.jump(self.dNodes[self.step]["val"])
            elif self.dNodes[self.step]["instruction"] == "notJmp":
                self.notJmp(self.dNodes[self.step]["val"])
            elif self.dNodes[self.step]["instruction"] == "yesJmp":
                self.yesJmp(self.dNodes[self.step]["val"])
            elif self.dNodes[self.step]["instruction"] == "lineWrite":
                print self.dNodes[self.step+1]
                self.lineWrite()
            self.step += 1
            print "Stack: " + str(self.stack)
        print self.stack

    def less(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = int(val1) < int(val2)
        self.push(tkn)

    def greater(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        tkn = int(val1) > int(val2)
        self.push(tkn)       

    def equals(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        print type(val1)
        if type(val1) is int:
            tkn = (int(val1) == int(val2))
        if type(val1) is str:
            tkn = val1 == val2
        self.push(tkn)

if __name__ == "__main__":
    main()
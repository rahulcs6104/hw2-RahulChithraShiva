import csv

def preorder(node,output):
    if node is None:
        return
    output.append(node.val)
    preorder(node.left,output)
    preorder(node.right,output)

def inorder(node,output,sign):
    if node is None:
        return
    if node.val in sign: #if it is a sign
        output.append("(")
        inorder(node.left,output,sign)
        output.append(node.val)
        inorder(node.right,output,sign)
        output.append(")")
    else:            #if it is a number
        output.append(node.val)

def postorder(node,output):
    if node is None:
        return
    postorder(node.left,output)
    postorder(node.right,output)
    output.append(node.val)



class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class HomeWork2:

    def constructBinaryTree(self, input) -> TreeNode:
        
        sign = ["+","-","/","*"]
        temp_stack = []

        for i in input:
            if i not in sign: #if it is a number
                num_node = TreeNode(i)
                temp_stack.append(num_node)
            else:             #if it is a sign
                sign_node = TreeNode(i)
                sign_node.right = temp_stack.pop()
                sign_node.left = temp_stack.pop()
                temp_stack.append(sign_node)
        return temp_stack.pop()

    #preorder of the elements of the tree, uses a helper function called preorder[it is in the top of the file , outside the class]
    def prefixNotationPrint(self, head: TreeNode) -> list:
        output=[]
        preorder(head,output)
        return output

    #inorder of the elements of the tree, uses a helper function called inorder[it is in the top of the file , outside the class]
    #little different concept for using the '(' and ')'
    def infixNotationPrint(self, head: TreeNode) -> list:
        output=[]
        sign = ["+","-","/","*"]
        inorder(head,output,sign)
        return output


    #postorder of the elements of the tree, uses a helper function called postorder[it is in the top of the file , outside the class]
    def postfixNotationPrint(self, head: TreeNode) -> list:
        output=[]
        postorder(head,output)
        return output


class Stack:

    #i have kept a variable called count to keep track of the size.
    #couldn't name it size as it has a conflict with the size function.
    def __init__(self):
        self.list=[]
        self.count = 0
        self.top = -1 

    def push(self,value):
        self.list.append(value)
        self.count += 1
        self.top += 1


    def pop(self):
        if self.count == 0:
            raise IndexError("Stack is empty , cannot pop") #raises an error here as there is no element to pop or remove
        pop_num = self.list[self.top]
        self.list.pop()
        self.count -= 1
        self.top -= 1
        return pop_num

    def size(self):
        return self.count
    
    def is_empty(self):
        return self.count == 0


    def evaluatePostfix(self,exp: str) -> int:
        lst = exp.split()
        if len(lst) == 0: #empty postfix expression edge case(if the input is empty) [edge case]
            raise ValueError("Empty postfix expression")
        sign = ["+","-","/","*"]
        for i in lst:
            if i not in sign: #i is a number
                try:
                    self.push(int(i)) #negative values also handled [edge case]
                except ValueError: #if the value is invalid like "1df4" [edge case]
                    raise ValueError(f"Invalid value = {i}")
            else:           #i is a sign
                try:
                    right = self.pop() #negative values also handled [edge case]
                    left = self.pop()#negative values also handled [edge case]
                except IndexError:   #if the stack doesn't have enough variables to pop [edge case]
                    raise ValueError("Malformed postfix expression")
                match i: #switch case to do coorect operation based on the sign
                    case "+":
                        self.push(left+right) 
                    case "-":
                        self.push(left-right)
                    case "*":
                        self.push(left*right)
                    case "/":
                        if right == 0:#dividing by zero will result is infinity , so raise an error [edge case]
                            raise ZeroDivisionError("The denominator is 0 and will result in infinity")
                        num = int(left/right)#negative values also handled [edge case]
                        self.push(num)
        if self.count != 1: #if the stack has more number or sign left than what can be handled [edge case]
            raise ValueError("Malformed postfix expression")
        return self.pop()


# Main Function. Do not edit the code below
if __name__ == "__main__":
    homework2 = HomeWork2()

    print("\nRUNNING TEST CASES FOR PROBLEM 1")
    testcases = []
    try:
        with open('p1_construct_tree.csv', 'r') as f:
            testcases = list(csv.reader(f))
    except FileNotFoundError:
        print("p1_construct_tree.csv not found")

    for i, (postfix_input,) in enumerate(testcases, 1):
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)
        output = homework2.postfixNotationPrint(root)

        assert output == postfix, f"P1 Test {i} failed: tree structure incorrect"
        print(f"P1 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 2")
    testcases = []
    with open('p2_traversals.csv', 'r') as f:
        testcases = list(csv.reader(f))

    for i, row in enumerate(testcases, 1):
        postfix_input, exp_pre, exp_in, exp_post = row
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)

        assert homework2.prefixNotationPrint(root) == exp_pre.split(","), f"P2-{i} prefix failed"
        assert homework2.infixNotationPrint(root) == exp_in.split(","), f"P2-{i} infix failed"
        assert homework2.postfixNotationPrint(root) == exp_post.split(","), f"P2-{i} postfix failed"

        print(f"P2 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 3")
    testcases = []
    try:
        with open('p3_eval_postfix.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                testcases.append(row)
    except FileNotFoundError:
        print("p3_eval_postfix.csv not found")

    for idx, row in enumerate(testcases, start=1):
        expr, expected = row

        try:
            s = Stack()
            result = s.evaluatePostfix(expr)
            if expected == "DIVZERO":
                print(f"Test {idx} failed (expected division by zero)")
            else:
                expected = int(expected)
                assert result == expected, f"Test {idx} failed: {result} != {expected}"
                print(f"Test case {idx} passed")

        except ZeroDivisionError:
            assert expected == "DIVZERO", f"Test {idx} unexpected division by zero"
            print(f"Test case {idx} passed (division by zero handled)")
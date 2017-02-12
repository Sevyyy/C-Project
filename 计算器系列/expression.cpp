
#include<iostream>
#include<map>
#include<algorithm>
#include<cmath>
#include<string>
#include<cstring>
#include<iomanip>
#include<sstream>
#include<stack>
#include<set>

using namespace std;

struct Node                                    //树节点定义
{
	double data;
	char oprt;
	char var;
	int tag;                                  //1是数据2是变量3是加减4是乘除5是幂
	Node * left;
	Node * right;
	Node() :left(NULL), right(NULL) {}
};

Node * copy_a_tree(Node * p)
{
	Node * ans = new Node();
	stack<Node *> src, des;
	if (p->tag == 1)
		ans->data = p->data;
	else if (p->tag == 2)
		ans->var = p->var;
	else
		ans->oprt = p->oprt;
	ans->tag = p->tag;
	src.push(p);
	des.push(ans);
	while (!src.empty())
	{
		Node * psrc = src.top();
		Node * pdes = des.top();
		des.pop();
		src.pop();
		if (psrc->right != NULL)
		{
			src.push(psrc->right);
			pdes->right = new Node();
			if (psrc->right->tag == 1)
				pdes->right->data = psrc->right->data;
			else if (psrc->right->tag == 2)
				pdes->right->var = psrc->right->var;
			else
				pdes->right->oprt = psrc->right->oprt;
			pdes->right->tag = psrc->right->tag;
			des.push(pdes->right);
		}
		if (psrc->left != NULL)
		{
			src.push(psrc->left);
			pdes->left = new Node();
			if (psrc->left->tag == 1)
				pdes->left->data = psrc->left->data;
			else if (psrc->left->tag == 2)
				pdes->left->var = psrc->left->var;
			else
				pdes->left->oprt = psrc->left->oprt;
			pdes->left->tag = psrc->left->tag;
			des.push(pdes->left);
		}
	}
	return ans;
}

class Expression
{
private:
	string prefix;              //前缀表达式
	stack<double> num_s;                        //运算数栈
	map<char, double> variable;                      //26个变量
protected:
	Node * expr;                               //存储表达式的二叉树（用于友元函数）
	set<char> variable_exist;                         //表达式所含变量
public:
	Expression()
	{
		prefix = "";
		for (char ch = 'a'; ch <= 'z'; ch++)
			variable[ch] = 0;
		expr = new Node();
	}
	~Expression()
	{
		while (!num_s.empty())
			num_s.pop();
	}
	bool is_operator(char op)                     //判断是否为操作符
	{
		if (op == '+' || op == '-' || op == '*' || op == '/' || op == '^')
			return true;
		else
			return false;
	}
	bool is_var(char v)                               //判断是否为变量
	{
		if (v >= 'a' && v <= 'z')
			return true;
		return false;
	}
	int isp(char ch)
	{
		switch (ch)
		{
		case '#':
			return 0;
			break;
		case '(':
			return 1;
			break;
		case '*': case '/':
			return 5;
			break;
		case '+':case '-':
			return 3;
			break;
		case ')':
			return 8;
			break;
		case'^':
			return 6;
			break;
		}
	}
	int icp(char ch)
	{
		switch (ch)
		{
		case '#':
			return 0;
			break;
		case '(':
			return 8;
			break;
		case '*': case '/':
			return 4;
			break;
		case '+':case '-':
			return 2;
			break;
		case ')':
			return 1;
			break;
		case'^':
			return 7;
			break;
		}
	}
	double converse_function_to_value(string s)                           //把三角函数的调用转换成计算结果（暂时不支持对未知数调用三角函数）
	{
		double pi = 4 * atan(1);
		stringstream stst;
		stst << s;
		char ch;
		while (stst >> ch)
		{
			if (ch == '(')
				break;
		}
		double v;
		stst >> v;
		if (s[0] == 't')
			return tan(v / 180 * pi);
		else if (s[0] == 's')
			return sin(v / 180 * pi);
		else if (s[0] == 'c')
			return cos(v / 180 * pi);
	}
	void read_expr()
	{
		cout << "请输入前缀表达式：";
		getline(cin, prefix);
	}
	void assign(char ch, double val)
	{
		variable[ch] = val;
	}
	void assign_all_variable()                           //为表达式内的变量赋值
	{
		if (variable_exist.size() == 0)
			return;
		cout << "请为变量赋值" << endl;
		set<char>::iterator it;
		for (it = variable_exist.begin(); it != variable_exist.end(); it++)
		{
			cout << *it << "=";
			double v;
			cin >> v;
			assign(*it, v);
		}
	}
	void prefix_to_tree()                                           //前缀表达式构造二叉树
	{
		stringstream sstr;
		sstr << prefix;
		stack<Node*> s;
		s.push(expr);
		Node * current;
		char op;
		string f;
		while (!s.empty())
		{
			current = s.top();
			s.pop();
			sstr >> f;
			if (f.size() > 1)
			{
				double data_out = converse_function_to_value(f);
				current->data = data_out;
				current->tag = 1;
				continue;
			}
			else
				sstr.putback(f[0]);
			sstr >> op;
			if (is_operator(op))
			{
				current->left = new Node();
				current->right = new Node();
				s.push(current->right);
				s.push(current->left);
				current->oprt = op;
				if (op == '+' || op == '-')
					current->tag = 3;
				else if (op == '*' || op == '/')
					current->tag = 4;
				else if (op == '^')
					current->tag = 5;
			}
			else if (is_var(op))
			{
				current->var = op;
				current->tag = 2;
				variable_exist.insert(op);
			}
			else
			{
				sstr.putback(op);
				double d;
				sstr >> d;
				current->data = d;
				current->tag = 1;
			}
		}
	}
	void print_nifix(Node * tree)                             //递归有括号，由二叉树输出中缀表达式
	{
		if (tree != NULL)
		{
			if (tree->left != NULL && tree->left->tag > 2 && tree->tag > tree->left->tag)
			{
				cout << '(';
				print_nifix(tree->left);
				cout << ')';
			}
			else
				print_nifix(tree->left);

			if (tree->tag > 2)
				cout << tree->oprt;
			else if (tree->tag > 1)
				cout << tree->var;
			else
				cout << tree->data;

			if (tree->right != NULL && tree->right->tag > 2 && tree->tag > tree->right->tag)
			{
				cout << '(';
				print_nifix(tree->right);
				cout << ')';
			}
			else
				print_nifix(tree->right);
		}
	}
	void print_nifix_out()                                    //把中缀表达式输出到控制台
	{
		cout << "对应的中缀表达式是：";
		print_nifix(expr);
		cout << endl;
	}
	void calculate_by_postfix(Node * tree)                              //通过后序遍历计算表达式的值（递归）
	{
		if (tree != NULL)
		{
			calculate_by_postfix(tree->left);
			calculate_by_postfix(tree->right);
			if (tree->tag == 1)
				num_s.push(tree->data);
			else if (tree->tag == 2)
				num_s.push(variable[tree->var]);
			else
			{
				double right = num_s.top();
				num_s.pop();
				double left = num_s.top();
				num_s.pop();
				switch (tree->oprt)
				{
				case '+':
					num_s.push(left + right);
					break;
				case '-':
					num_s.push(left - right);
					break;
				case '*':
					num_s.push(left * right);
					break;
				case '/':
					num_s.push(left / right);
					break;
				case'^':
					num_s.push(pow(left, right));
					break;
				}
			}
		}
	}
	void compute()                                              //执行计算并输出
	{
		while (!num_s.empty())
			num_s.pop();
		calculate_by_postfix(expr);
		cout << "表达式计算的结果是：";
		cout << num_s.top();
		cout << endl;
	}
	void merge_const_a_tree(Node * tree)                          //化简一棵树（用于递归）
	{
		if (tree->left->tag >= 3)
			merge_const_a_tree(tree->left);
		if (tree->right->tag >= 3)
			merge_const_a_tree(tree->right);
		if (tree->tag >= 3 && tree->left->tag == 1 && tree->right->tag == 1)
		{
			tree->tag = 1;
			double ans;
			switch (tree->oprt)
			{
			case '+':
				ans = tree->left->data + tree->right->data;
				break;
			case '-':
				ans = tree->left->data - tree->right->data;
				break;
			case '*':
				ans = tree->left->data * tree->right->data;
				break;
			case '/':
				ans = tree->left->data / tree->right->data;
				break;
			case '^':
				ans = pow(tree->left->data, tree->right->data);
				break;
			}
			tree->data = ans;
			delete tree->left;
			delete tree->right;
			tree->left = NULL;
			tree->right = NULL;
		}
		return;
	}
	void merge_const()                                     //化简表达式
	{
		merge_const_a_tree(expr);
	}

	friend Expression compound(char op, Expression e1, Expression e2);
};

Expression compound(char op, Expression e1, Expression e2)
{
	Expression ans;
	ans.expr = new Node();
	if (op == '+' || op == '-')
		ans.expr->tag = 3;
	else if (op == '*' || op == '/')
		ans.expr->tag = 4;
	else
		ans.expr->tag = 5;
	ans.expr->oprt = op;
	ans.expr->left = copy_a_tree(e1.expr);
	ans.expr->right = copy_a_tree(e2.expr);
	ans.variable_exist.insert(e1.variable_exist.begin(), e1.variable_exist.end());
	ans.variable_exist.insert(e2.variable_exist.begin(), e2.variable_exist.end());
	return ans;
}

int main()
{
	Expression a, b, c;
	a.read_expr();
	a.prefix_to_tree();
	a.print_nifix_out();
	a.print_nifix_out();
	a.assign_all_variable();
	a.compute();

	cin.get();

	b.read_expr();
	b.prefix_to_tree();
	b.print_nifix_out();
	b.print_nifix_out();
	b.assign_all_variable();
	b.compute();

	cout << "请输入合并的操作符: ";
	char op;
	cin >> op;
	c = compound(op, a, b);
	c.print_nifix_out();
	c.merge_const();
	cout << "进行化简后：";
	c.print_nifix_out();
	c.assign_all_variable();
	c.print_nifix_out();
	c.compute();
	return 0;
}

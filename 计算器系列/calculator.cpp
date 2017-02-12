#include<iostream>
#include<cmath>
#include<stack>
#include<string>
#include<cstring>
#include<iomanip>
#include<sstream>

using namespace std;

void print_stack(stack<char> s)
{
	stack<char> t;
	while (!s.empty())
	{
		t.push(s.top());
		s.pop();
	}
	while (!t.empty())
	{
		cout << t.top();
		t.pop();
	}
}             //输出字符栈
void print_stack(stack<double> s)
{
	stack<double> t;
	while (!s.empty())
	{
		t.push(s.top());
		s.pop();
	}
	while (!t.empty())
	{
		cout << t.top()<<" ";
		t.pop();
	}
}                           //输出浮点数栈
class calculator
{
private:
	stack<double> s;      //运算数栈
	string nifix;           //中缀表达式
	string postfix;           //后缀表达式
public:
	calculator()                   
	{
		nifix = "";
		postfix = "";
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
	bool is_not_digit(char c)
	{
		if (!isdigit(c) && c != '.')
			return true;
		return false;
	}
	void ni_to_post()
	{
		cout << "中缀转后缀：" << endl;
		cout << "扫描项  " << "项类型   "<< "动作   " << "栈的变化          " << "输出" << endl;
		stack<char> st;
		char ch, chl;
		st.push('#');
		int n = nifix.size();
		int index = 0;
		ch = nifix[0];
		while (index < n && !st.empty())
		{
			int type = 1;      //0是操作数1是操作符
			int in_or_out = 0;     //0是in,1是out,2是空
			if ((ch < '0' || ch > '9') && ch != '.')
			{
				postfix += ' ';
				chl = st.top();
				if (isp(chl) < icp(ch))
				{
					st.push(ch);
					index++;
				}
				else if (isp(chl) > icp(ch))
				{
					in_or_out = 1;
					postfix += chl;
					st.pop();
				}
				else
				{
					in_or_out = 1;
					st.pop();
					if (chl == '(')
						index++;
				}
			}
			else
			{
				in_or_out = 2;
				type = 0;
				postfix += ch;
				index++;
			}
			cout << ch << "        ";
			cout << (type == 0 ? "操作数" : "操作符") << "   ";
			if (in_or_out != 2)
				cout << (in_or_out == 0 ? "进栈" : "出栈") << "   ";
			else
				cout << "        " ;
			print_stack(st);
			cout<<"              "<< postfix << endl;
			ch = nifix[index];
		}

	}
	void print_ans()
	{
		nifix.pop_back();
		cout << fixed<<nifix << " = " << s.top() << endl;
	}
	void clear()
	{
		while (!s.empty())
			s.pop();
	}
	void add_operand(double value)
	{
		s.push(value);
	}
	bool get_two_operands(double & left, double & right)
	{
		if (s.empty())
			return false;
		right = s.top();
		s.pop();
		if (!s.empty())
		{
			left = s.top();
			s.pop();
		}
		else
			left = 0;
		return true;
	}
	void do_operator(char op)
	{
		double left, right, value;
		bool result;
		result = get_two_operands(left, right);
		if (result == true)
		{
			switch (op)
			{
			case '+':
				value = left + right;
				s.push(value);
				break;
			case '-':
				value = left - right;
				s.push(value);
				break;
			case '*':
				value = left * right;
				s.push(value);
				break;
			case '/':
				if (right == 0.0)
					clear();
				else
				{
					value = left / right;
					s.push(value);
				}
				break;
			case'^':
				value = pow(left, right);
				s.push(value);
				break;
			}
		}
		else
			clear();
	}
	void run()
	{
		cout << "请输入算式：";
		cin >> nifix;
		if (!isdigit(nifix[0]))
			nifix = '0' + nifix;
		nifix += '#';
		ni_to_post();
		cout << "开始运算：" << endl;
		cout << "扫描项  " << "项类型   " << "动作                                     " << "栈内容" << endl;
		stringstream sstr;
		sstr << postfix;
		char ch;
		double new_operand;
		while (sstr >> ch && ch != '#' )
		{
			int type = 1;      //0是操作数1是操作符
			int in_or_out = 0;     //0是in,1是out,2是具体操作

			switch (ch)
			{
			case '+':case '-':case '*' : case '/':case'^':
				in_or_out = 2;
				cout << ch<<"        ";
				do_operator(ch);
				break;
			default:
				type = 0;
				in_or_out = 0;
				sstr.putback(ch);
				sstr >> new_operand;
				cout << new_operand<<"        ";
				add_operand(new_operand);
			}
			cout << (type == 0 ? "操作数" : "操作符") << "   ";
			if (in_or_out != 2)
			{
				cout << (in_or_out == 0 ? "进栈                                     " : "出栈") << "   ";
			}
			else
			{
				cout << "去上一步栈的后两个数进行运算，结果进栈        ";
			}
			print_stack(s);
			cout << endl;
		}
	}
};

int main()
{
	while (1)
	{
		calculator cal;
		cal.clear();
		cal.run();
		cal.print_ans();
		cal.clear();
		cin.get();
		cin.get();
		system("cls");
	}
	return 0;
}

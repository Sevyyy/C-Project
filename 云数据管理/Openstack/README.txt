1、先配置openrc配置文件  （#source openrc）
2、命令行为./dosth option  (先#chmod 777 dosth） 
    option可输入以下：
	help           : show the help list
	service_list   : show the list of all services
	role_list      : show the list of all roles
	endpoint_list  : show the list of all endpoints
	tenant_list    : show the list of all tenants
	user_list      : show the list of all users
	add_tenant     : add a tenant with some input
	add_user_role  : add a role and user with some input
	add_service_endpoint    : add a service and endpoint with some input
    （PS： 命令行dosth help即可查看帮助）

3、本代码参照官方API编写，并加入了一些简单必要的脚本逻辑控制，实现了要求的功能以及一个额外功能
（http://docs.openstack.org/developer/python-keystoneclient/using-api-v2.html）

4、openrc配置文件是从openstack dashboard上直接下载的，不用手动输入
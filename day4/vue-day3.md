# vue-day3

## 1. vue路由

> vue的页面是由多个组件组成的，一个vue项目只需要一张html页面，而页面中不同部分的展示其实就是通过vue的路由来切换不同的组件

### 1.1 路由的使用

~~~vue
<div id="app">

    <h3>这是主页的页头</h3>
    <hr>
    <!-- 定义路由访问不同组件的链接  通过to="/路由地址"来指定当前标签要访问的组件   -->
    <router-link to="/first">访问系统首页</router-link>
    <router-link to="/second">访问用户页</router-link>

    <!--指定路由对应组件出现的位置-->
    <router-view></router-view>

</div>

<script src="js/vue.min.js"></script>
<!--依赖于vue.js才可以使用-->
<script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
<script>

    let first = {
        template: `
            <div>百知教育管理系统</div>
        `
    }

    let second = {
        template: `
            <div>学生管理</div>
        `
    }

    // 为每个组件准备对应的路由  定义组件与路由的映射关系
    // 页面中输入路由来显示对应的组件
    // 需要将定义好的路由注入到当前vue实例中
    let myRouter = new VueRouter({
        routes: [
            // path指的是访问组件的地址  component代表这个地址对应的组件  一一对应
            {path: "/first", component: first},
            {path: "/second", component: second}
        ]
    })

    new Vue({
        el: "#app",
        data: {},
        // 注入定义好的vue路由
        // 通过router配置参数注入,从而整个vue实例都拥有路由功能
        router: myRouter
    })
</script>
~~~

~~~markdown
# 总结：
	1. 需要为每个组件通过一一对应的方式来建立路由映射  new VueRouter
	2. 需要将定义好的路由映射注入到vue的实例中  router: 变量名
	3. 需要在指定的位置使用 router-view标签来选择组件展示的位置
	4. 可以通过router-link来发起访问不同组件的路由
~~~



### 1.2 路由的应用

~~~vue
<div id="app">

    <h2>系统欢迎页</h2>
    <router-link to="/index">首页</router-link>
    <router-link to="/user">用户</router-link>
    <hr>

    <router-view></router-view>

</div>

<script src="js/vue.min.js"></script>
<script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
<script>

    let index = {
        template: `
            <div>
            <h4>这是index页面</h4>
            <h3>欢迎访问信息管理系统</h3>
</div>
        `
    }

    let user = {
        template: `
          <div>
          <h3>用户列表页</h3>
          <table border="2">
            <tr>
              <td>ID</td>
              <td>姓名</td>
              <td>生日</td>
              <td>操作</td>
            </tr>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.bir }}</td>
              <td>删除 | 更新</td>
            </tr>
          </table>
          </div>
        `,
        data() {
            return {
                users: [
                    {"id": 1, username: "小黑", bir: "2013-12-12"},
                    {"id": 2, username: "小波", bir: "2014-11-12"},
                    {"id": 3, username: "小广", bir: "2015-10-12"},
                ]
            }
        },
    }

    let myRouter = new VueRouter({
        routes: [
            {path: "/index", component: index},
            {path: "/user", component: user},
            // 当路由匹配到 / 将重定向到首页
            {path: "/", redirect: "/index"},
            // 当用户的路由没有匹配到任何地址时  重定向到首页  要放到路由的末尾
            {path: "/*", redirect: "/index"}
        ]
    })


    new Vue({
        el: "#app",
        data: {},
        router: myRouter,
    })
</script>
~~~

## 2. 路由的参数传递

> 127.0.0.1:8000/user/get_user/?id=1
>
> 127.0.0.1:8000/user/get_user/1/

### 2.1 query拼接传参

> 1. 在通过`<router-link to="路径地址">`发起访问请求时,可以在路径后通过?拼接的形式传递参数
> 2. 拼接传参的形式需要在对应的组件内部通过`{{$route.query.参数名}}`取值



~~~vue
<div id="app">

    <router-view></router-view>

</div>

<script src="js/vue.min.js"></script>
<script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
<script>

    let first = {
        template: `
            <div>
                这是组件1
                <router-link to="/second?id=3&name=tom">查看组件2的这一页</router-link>
</div>
        `
    }

    let second = {
        template: `
            <div>这是组件2: 需要接受组件1传递过来的id--->: {{ $route.query.id }}
            <br>
            这是上个组件传递的用户名--->: {{$route.query.name}}
            </div>

        `
    }

    let myRouter = new VueRouter({
        routes: [
            {path: "/first", component: first},
            {path: "/second", component: second},
            {path: "/", redirect: "/first"},
        ]
    })

    new Vue({
        el: "#app",
        data: {},
        router: myRouter,
    })
</script>
~~~

### 2.2 动态路由传参

> 所谓的动态路由传参,就是将参数作为路由的一部分传递

~~~vue
<div id="app">

    <router-view></router-view>

</div>

<script src="js/vue.min.js"></script>
<script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
<script>

    let first = {
        template: `
            <div>
            这是组件1
            <router-link to="/second/1/tom">访问组件2</router-link>
</div>
        `
    }

    let second = {
        template: `
            <div>
            这是组件2: 接受组件1传递的id--->: {{$route.params.id}}
            <br>
            这是组件1传递的用户名---> {{$route.params.name}}

</div>
        `
    }

    let myRouter = new VueRouter({
        routes: [
            {path: "/first", component: first},
            {path: "/second/:id/:name", component: second},
            {path: "/", redirect: "/first"},
        ]
    })
    new Vue({
        el: "#app",
        data: {},
        router: myRouter,
    })
</script>
~~~

~~~markdown
# 总结:
	1. 动态路由传参需要将参数包含在路径中
	2. 在定义路由时需要按位置匹配好参数 <router-link to="/second/1/tom"> 需要与你的路由地址一一匹配
	3. 参数需要使用{{$route.params.参数名接受}}
~~~

### 2.3 js跳转传参

> 1. 通过拼接传参在接受的时候使用` {{ $route.query.参数名}}`
> 2. 通过动态路由传参需要使用` {{ $route.params.参数名}}`接受

~~~vue
<div id="app">

    <router-view></router-view>

</div>

<script src="js/vue.min.js"></script>
<script src="https://unpkg.com/vue-router/dist/vue-router.js"></script>
<script>

    let com = {
        template: `
          <div>
          这是组件1
          <button @click="goPage">跳转到用户页面</button>
          </div>
        `,
        methods: {
            goPage() {
                // 可以通过此方法跳转组件
                // this.$router.push("/com2?id=4")
                // this.$router.push("/com2/1")
                this.$router.push({path: "/com2/1"});
            }
        }
    }

    let com2 = {
        template: `
        <div>这组件2: 接受组件1传递的参数--->{{$route.query.id}}
            <div>这组件2: 接受组件1动态路由参数--->{{$route.params.id}}</div>
        </div>
        `
    }

    let myRouter = new VueRouter({
        routes: [
            {path: "/com", component: com},
            {path: "/com2/:id", component: com2},
            {path: "/", redirect: "/com"},
        ]
    })

    new Vue({
        el: "#app",
        data: {},
        router: myRouter,
    })
</script>
~~~

### 2.4   route 与 router的区别

> `$route`对象是当前路由的信息对象, 可以通过`$route.query|$route.params`来获取当前路径所包含的参数, 使用`$route.path`可以获取当前路由的路径
>
> `$router`对象是控制整个路由系统的对象, 切换路径的操作都是由此对象完成的.  `router-link`标签是一种快捷方式
<template>
    <div class="header-box">
        <div class="header">
            <div class="content">
                <div class="logo full-left">
                    <router-link to="/"><img src="../../../static/image/logo.png" alt=""></router-link>
                </div>
                <ul class="nav full-left">
                    <li  v-for="(header,index) in header_list" :id="index" >
                        <a :href="header.link" v-if="header.is_site">{{header.title}}</a><router-link v-else :to="header.link">{{header.title}}</router-link></li>
                </ul>
                <!-- 用户登录情况下               -->
                <div class="login-bar full-right" v-if="token">
                    <div class="shop-cart full-left">
                        <img src="/static/image/cart.svg" alt="">
                        <span><router-link to="/cart">{{this.$store.state.cart_length}}购物车</router-link></span>
                    </div>
                    <div class="login-box full-left">
                        <span id="s1">Hi,{{user}}</span>
                        <router-link to="login/">个人中心</router-link>
                        &nbsp;|&nbsp;
                        <span @click="exit">退出登录</span>
                    </div>
                </div>
                <!--用户未登录情况下                -->
                <div class="login-bar full-right" v-else>
                    <div class="shop-cart full-left">
                        <img src="/static/image/cart.svg" alt="">
                        <span><router-link to="/cart">购物车</router-link></span>
                    </div>
                    <div class="login-box full-left">
                        <router-link to="login/">登录</router-link>
                        &nbsp;|&nbsp;
                        <router-link to="register/">注册</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "Header",
    data(){
        return{
            header_list:[],
            token:"",
            user:"",
        }
    },
    methods:{
        //退出登录
        exit(){
            localStorage.token=""
            localStorage.user=""
            this.token=""

        },
        //获取所有导航栏
        get_all_header(){
            this.$axios.get("http://127.0.0.1:8000/home/header/").then(response=>{
                this.header_list = response.data
            })
        },
        //获取用户登录信息
        get_user(){
            this.token = localStorage.token;
            this.user = localStorage.user;
        },
        get_cart_num(){
                this.$axios({
                    url: "http://127.0.0.1:8000/cart/cart/",
                    method: "delete",
                    data: {
                        courser_id: 1,
                        delete_course: "1",
                        user_id:localStorage.id
                    },
                }).then(res => {
                    this.$store.commit("add_cart", res.data.cart_length);
                })
            },
    },
    created() {
        this.get_all_header()
        this.get_user()
        this.get_cart_num()
    }
}
</script>

<style scoped>
#s1{
    color: red;
    font-size: small;
    font-weight: bold;
}
.header-box {
    height: 80px;
}

.header {
    width: 100%;
    height: 80px;
    box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    margin: auto;
    z-index: 99;
    background: #fff;
}

.header .content {
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
}

.header .content .logo {
    height: 80px;
    line-height: 80px;
    margin-right: 50px;
    cursor: pointer; /* 设置光标的形状为爪子 */
}

.header .content .logo img {
    vertical-align: middle;
}

.header .nav li {
    float: left;
    height: 80px;
    line-height: 80px;
    margin-right: 30px;
    font-size: 16px;
    color: #4a4a4a;
    cursor: pointer;
}

.header .nav li span {
    padding-bottom: 16px;
    padding-left: 5px;
    padding-right: 5px;
}

.header .nav li span a {
    display: inline-block;
}

.header .nav li .this {
    color: #4a4a4a;
    border-bottom: 4px solid #ffc210;
}

.header .nav li:hover span {
    color: #000;
}

.header .login-bar {
    height: 80px;
}

.header .login-bar .shop-cart {
    margin-right: 20px;
    border-radius: 17px;
    background: #f7f7f7;
    cursor: pointer;
    font-size: 14px;
    height: 28px;
    width: 100px;
    margin-top: 30px;
    line-height: 32px;
    text-align: center;
}

.header .login-bar .shop-cart:hover {
    background: #f0f0f0;
}

.header .login-bar .shop-cart img {
    width: 15px;
    margin-right: 4px;
    margin-left: 6px;
}

.header .login-bar .shop-cart span {
    margin-right: 6px;
}

.header .login-bar .login-box {
    margin-top: 33px;
}

.header .login-bar .login-box span {
    color: #4a4a4a;
    cursor: pointer;
}

.header .login-bar .login-box span:hover {
    color: #000000;
}

a {
    text-decoration: none;
    color: #333;
}

.member {
    display: inline-block;
    height: 34px;
    margin-left: 20px;
}

.member img {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: inline-block;
}

.member img:hover {
    border: 1px solid yellow;
}

.header .login-bar .login-box1 {
    margin-top: 16px;
}

a:hover {
    display: inline-block;
}
</style>

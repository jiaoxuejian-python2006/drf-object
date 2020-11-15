<template>
    <div class="cart">
        <Header></Header>
        <div class="cart_info">
            <div class="cart_title">
                <span class="text">我的购物车</span>
                <span class="total">共4门课程</span>
            </div>
            <div class="cart_table">
                <div class="cart_head_row">
                    <span class="doing_row"></span>
                    <span class="course_row">课程</span>
                    <span class="expire_row">有效期</span>
                    <span class="price_row">单价</span>
                    <span class="do_more">操作</span>
                </div>
                <div class="cart_course_list">
                    <CartItem v-for="char in char_list" :char="char" @change_selected="change_selected"
                              @delete_course="delete_course" @change_expire="change_expire"></CartItem>
                </div>
                <div class="cart_footer_row">
                    <span class="cart_select" ><label> <el-checkbox v-model="checked" @change="checked_all"></el-checkbox>&nbsp&nbsp&nbsp<span
                        >全选</span></label></span>
                    <span class="cart_delete"><i class="el-icon-delete"></i> <span @click="delete_all">删除</span></span>
                    <span class="goto_pay"><router-link to="/order">去结算</router-link></span>
                    <span class="cart_total">总计：¥{{ price }}</span>
                </div>
            </div>
        </div>
        <Footer></Footer>
    </div>
</template>
<script>

import CartItem from "./CartItem";
import Footer from "./common/Footer";
import Header from "./common/Header";

export default {
    name: "Cart",
    data() {
        return {
            checked: "",
            char_list: [],
            price: 0
        }
    },
    methods: {
        //子传父 修改每一个商品的选择状态 同时改变对应的总价格
        change_selected(id) {
            this.$axios({
                url: "http://127.0.0.1:8000/cart/cart/",
                method: "delete",
                data: {
                    courser_id: id,
                    user_id:localStorage.id
                },
            }).then(res => {
                for (let i = 0; i < this.char_list.length; i++) {
                    if (this.char_list[i].id === id) {
                        if (this.char_list[i].selected) {
                            this.price = parseFloat(this.price)
                            this.price += parseFloat(this.char_list[i].price)
                            this.price = parseFloat(this.price.toFixed(2))
                        } else {
                            this.price = parseFloat(this.price)
                            this.price -= parseFloat(this.char_list[i].price)
                            this.price = parseFloat(this.price.toFixed(2))
                        }
                    }
                }
                //判断购物车中所有商品是否为选中状态，如果是全部选中，则全选为true 否则全选为false
                var count = 0
                for (let i = 0; i < this.char_list.length; i++) {
                    if (this.char_list[i].selected) {
                        count++
                    }
                }

                if (count === this.char_list.length) {
                    this.checked = true
                } else {
                    this.checked = false
                }
            })
        },
        //子传父 删除某一个商品
        delete_course(id) {
            this.$axios({
                url: "http://127.0.0.1:8000/cart/cart/",
                method: "delete",
                data: {
                    courser_id: id,
                    delete_course: "1",
                    user_id:localStorage.id
                },
            }).then(res => {
                for (let i = 0; i < this.char_list.length; i++) {
                    if (this.char_list[i].id === id) {
                        this.price = (this.price - parseFloat(this.char_list[i].price)).toFixed(2)
                        this.char_list.splice(i, 1)
                    }
                }
                this.$message.success(res.data.message)
                this.$store.commit("add_cart", res.data.cart_length);

            })
        },
        // 子传父 修改change_expire 修改有效期和对应的价格
        change_expire(expire_id, courser_id) {
            // alert(courser_id)
            this.$axios({
                url: "http://127.0.0.1:8000/cart/cart/",
                method: "put",
                data: {
                    expire_id: expire_id,
                    courser_id: courser_id,
                    user_id:localStorage.id
                },
            }).then(res => {
                for (let i = 0; i < this.char_list.length; i++) {
                    if (this.char_list[i].id === res.data.courser_id) {
                        this.char_list[i].price = res.data.price
                    }
                }
                let num = 0
                for (let i = 0; i < this.char_list.length; i++) {
                    num += parseFloat(this.char_list[i].price)
                }
                this.price = num.toFixed(2)
            })
        },
        //进入购物车页面时获取购物车商品数据
        get_cart() {
            let token = this.check_user_login()
            this.$axios.get("http://127.0.0.1:8000/cart/cart/", {
                headers: {
                    "Authorization": "jwt " + token
                },
                params:{
                    user_id:localStorage.id
                }
            }).then(res => {
                this.char_list = res.data

                //计算总价钱
                var all_price = 0
                var count = 0
                for (let i = 0; i < this.char_list.length; i++) {
                    if (this.char_list[i].selected) {
                        count++
                        all_price = all_price + parseFloat(this.char_list[i].price)
                    }
                }
                this.price = all_price.toFixed(2)
                //定义count属性 判断进入到购物车页面时 商品是否为选中状态，若全部选中则checked属性为true 否则为false

                if (this.char_list.length===count){
                    this.checked = true
                }else {
                    this.checked = false
                }
            }).catch(error => {
            })
        },
        //检查用户是否登录
        check_user_login() {
            let token = localStorage.token || sessionStorage.token
            if (!token) {
                let self = this
                this.$confirm("请登陆后再添加购物车", {
                    callback() {
                        self.$router.push("/login");
                    }
                });
                return false
            }
            return token
        },
        //删除所有选中的商品  同时改变总价格为0
        delete_all() {
            this.$axios({
                url: "http://127.0.0.1:8000/cart/cart/",
                method: "delete",
                data: {
                    delete_course: "1",
                    delete_all: "1",
                },
            }).then(res => {
                for (let i = 0; i < this.char_list.length; i++) {
                    if (this.char_list[i].selected) {
                        // console.log(this.price,typeof (this.price));
                        // console.log(i);
                        // delete this.char_list[i]
                        // console.log(this.price);
                        // this.price = (this.price - parseFloat(this.char_list[i].price)).toFixed(2)
                        // this.price-=parseFloat(this.char_list[i].price)
                        this.char_list.splice(i, 1)
                        i--
                        // this.price=parseFloat(0)
                    }
                    this.price = parseFloat(0)
                }
                this.$message.success(res.data.message)
                this.$store.commit("add_cart", res.data.cart_length);
                //判断删除全部后 列表中是否有数据  如果有则将总价格设为0
                if (this.char_list.length) {
                    this.price = 0
                }
            })
        },
        //全选事件  点击则全部选中或全部取消
        checked_all() {
            for (let i = 0; i < this.char_list.length; i++) {
                this.char_list[i].selected = this.checked
            }
        },
    },
    created() {
        this.get_cart()
    },
    components: {
        CartItem: CartItem,
        Footer: Footer,
        Header: Header,
    }
}
</script>

<style scoped>
.cart_info {
    width: 1200px;
    margin: 0 auto 200px;
}

.cart_title {
    margin: 25px 0;
}

.cart_title .text {
    font-size: 18px;
    color: #666;
}

.cart_title .total {
    font-size: 12px;
    color: #d0d0d0;
}

.cart_table {
    width: 1170px;
}

.cart_table .cart_head_row {
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
    padding-right: 30px;
}

.cart_table .cart_head_row::after {
    content: "";
    display: block;
    clear: both;
}

.cart_table .cart_head_row .doing_row,
.cart_table .cart_head_row .course_row,
.cart_table .cart_head_row .expire_row,
.cart_table .cart_head_row .price_row,
.cart_table .cart_head_row .do_more {
    padding-left: 10px;
    height: 80px;
    float: left;
}

.cart_table .cart_head_row .doing_row {
    width: 78px;
}

.cart_table .cart_head_row .course_row {
    width: 530px;
}

.cart_table .cart_head_row .expire_row {
    width: 188px;
}

.cart_table .cart_head_row .price_row {
    width: 162px;
}

.cart_table .cart_head_row .do_more {
    width: 162px;
}

.cart_footer_row {
    padding-left: 30px;
    background: #F7F7F7;
    width: 100%;
    height: 80px;
    line-height: 80px;
}

.cart_footer_row .cart_select span {
    margin-left: -7px;
    font-size: 18px;
    color: #666;
}

.cart_footer_row .cart_delete {
    margin-left: 58px;
}

.cart_delete .el-icon-delete {
    font-size: 18px;
}

.cart_delete span {
    margin-left: 15px;
    cursor: pointer;
    font-size: 18px;
    color: #666;
}

.cart_total {
    float: right;
    margin-right: 62px;
    font-size: 18px;
    color: #666;
}

.goto_pay {
    float: right;
    width: 159px;
    height: 80px;
    outline: none;
    border: none;
    background: #ffc210;
    font-size: 18px;
    color: #fff;
    text-align: center;
    cursor: pointer;
}
</style>

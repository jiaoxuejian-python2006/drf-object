<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="char.selected" ></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img src="/static/image/python.jpg" alt="">
            <span><router-link to="/course/detail/1">{{char.name}}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="char.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select" >
                    <el-option :label="item.expire_text" :value="item.id" :key="item.id" v-for="item in char.expire_list"></el-option>
<!--                <el-option label="2个月有效" value="60" key="60"></el-option>-->
<!--                <el-option label="3个月有效" value="90" key="90"></el-option>-->
<!--                <el-option label="永久有效" value="10000" key="10000"></el-option>-->
            </el-select>
        </div>
        <div class="cart_column column_4">¥{{char.price}}</div>
        <div class="cart_column column_4" @click="delete_course">删除</div>
    </div>
</template>
<script>
export default {
    name: "CartItem",
    data(){
        return{
            expire_id:"",
        }
    },
    props: ['char'],
    methods: {
        // 发起请求  在后台修改商品的选中状态
        // 课程id， 选中状态
        change_selected(){
            this.$emit("change_selected",this.char.id)
        },
        delete_course(){
            this.$emit("delete_course",this.char.id)
        },
        change_expire(){
            console.log(this.char.expire_id,this.char.id);
            this.$emit("change_expire",this.char.expire_id,this.char.id)
        }
    },
    watch: {
        "char.selected": function () {
            this.change_selected();
        },
        // 监测select框的有效期id的一旦发生变化，则发起修改有效期的请求
        "char.expire_id": function (){
            this.change_expire()
        },
    },
}
</script>

<style scoped>
.cart_item::after {
    content: "";
    display: block;
    clear: both;
}

.cart_column {
    float: left;
    height: 250px;
}

.cart_item .column_1 {
    width: 88px;
    position: relative;
}

.my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
}

.cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
}

.cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
}

.cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
}

.my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
}

.cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
}

</style>

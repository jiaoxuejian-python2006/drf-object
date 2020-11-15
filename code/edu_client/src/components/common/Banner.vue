<template>
    <div>
        <el-carousel height="720px" :interval="3000" arrow="always">
            <el-carousel-item v-for="(banner,index) in banner_list" :key="index">
                <img :src="banner.img" alt="">
            </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script>
export default {
    name: "Banner",
    data(){
        return{
            banner_list:[]
        }
    },
    methods:{
        get_all_banner(){
            this.$axios.get("http://127.0.0.1:8000/home/banner/").then(response=>{
            // this.$axios.get(this.$settings.HOST+"home/banner/").then(response=>{
                this.banner_list = response.data
            })
        }
    },
    created() {
        //获取轮播图数据
        this.get_all_banner()
    }
}
</script>

<style scoped>
.el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
}

.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
}
</style>

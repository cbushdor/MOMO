Vue.component('product-details',{
    props: {
        details: {
            type: Array,
            required: true,
        }
    },
    template: `
        <ul>
            <li v-for="detail in details">
                {{ detail }}
            </li>
        </ul> 
   `
})

Vue.component('product', {
    props:{
        premium: {
            type: Boolean,
            required: true,
        },
    },
    template: `
        <div class="product">
            <div class="product-image">
               <img v-bind:src="image" v-bind:alt="altText" />
            </div>
            <div class="product-info">
                <h2>{{ title }}</h2>
                <p v-if="inStock">In Stock</p>
                <p v-else  :class="{ outOfStock: !inStock }">Out of Stock</p>
                <p>Shipping: {{ shipping }}</p>
                <p>{{ printBrandProduct }}</p>
                <product-details :details="details"></product-details> 

                <div v-for="(variant,index) in variants" 
                    :key="variant.Id"
                    class="color-box"
                    :style="{ backgroundColor: variant.variantColor  }"
                    @mouseover="updateProduct(index)">
                </div> 
                <button v-on:click="addToCart" 
                        :disabled="!inStock"
                        :class="{ disabledButton: !inStock }">Add to cart</button>
                <button v-on:click="decrementFromCart">Remove from cart</button>
            </div>
        </div>
    `,
    data() {
        return {
            product: 'Socks',
            brand: 'Mastery vue',
            selectedVariant: 0,
            altText: "A pair of socks",
            inventory: 9,
            details: ['80% cotton', '20% polyester', 'Gender-neutral'],
            variants: [
                {
                    variantId: 2239,
                    variantColor: "green",
                    variantImage: './assets/vmSocks-green-onWhite.jpg',
                    variantQuantity: 10
                },
                {
                    variantId: 2235,
                    variantColor: "blue",
                    variantImage: './assets/vmSocks-blue-onWhite.jpg',
                    variantQuantity: 0
                },
            ],
            listOfSizes: ["XS", "S", "L", "M", "XL", "XXL"],
        }
    },
    methods: {
        addToCart() {
            this.$emit('add-to-cart',this.variants[this.selectedVariant].variantId)
        },
        decrementFromCart() {
            this.$emit('remove-from-cart', this.variants[this.selectedVariant].variantId)
        },
        updateProduct(index) {
            this.selectedVariant = index
            console.log(index)
        },
    },
    computed: {
        title() {
            return this.brand + ' ' + this.product
        },
        image() {
            return this.variants[this.selectedVariant].variantImage
        },
        inStock() {
            return this.variants[this.selectedVariant].variantQuantity
        },
        printBrandProduct() {
            return (this.onSale) ? this.brand + ' ' + this.product + " are on sale" + ' ' + this.onSale
                : this.brand + ' ' + this.product + " are not on sale" + ' ' + this.onSale
        },
        onSale() {
            return this.variants[this.selectedVariant].variantQuantity > 0
        },
        shipping() {
            if(this.premium){
                return "Free"
            }
            return 2.99
        },
    }
})

var app = new Vue({
    el: '#app',
    data: {
        premium: true,
        cart: [],
    },
    methods: {
        updateCart(id) {
            this.cart.push(id)
        },
        removeItem(id) {
            for(var i = this.cart.length - 1 ; i >= 0; i--){
                if(this.cart[i] === id){
                    this.cart.splice(i,1)
                }
            }
        },
    }

});
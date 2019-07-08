var app = new Vue({
    el: '#app',
    data: {
        product: 'Socks',
        image: './assets/vmSocks-green-onWhite.jpg',
        myUrl: '',
        altText: "A pair of socks",
        inStock: true,
        inventory: 9,
        details: ["80% cotton","20% polyester","Gender neutral"],
        variants: [
            {
                variantId: 2239, 
                variantColor: "green",
                variantImage: './assets/vmSocks-green-onWhite.jpg'
            },
            {
                variantId: 2235,
                variantColor: "blue",
                variantImage: './assets/vmSocks-blue-onWhite.jpg'
            },
        ],
        listOfSizes: ["XS","S","L","M","XL","XXL"],
        cart: 0,
    },
    methods: {
        addToCart: function () { 
            this.cart += 1 
        },
        updateProduct: function (variantImage) {
            this.image = variantImage
        }
    }

    
});
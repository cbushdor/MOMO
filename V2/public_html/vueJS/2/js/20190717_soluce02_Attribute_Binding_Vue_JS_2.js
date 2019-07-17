/*
------------------------------------------------------
* Created By : sdo
* File Name :
* Creation Date : Wed Jul 17 14:54:56 2019
* Last Modified : Wed Jul 17 14:55:15 2019
* Email Address : sdo@macbook-pro-de-sdo.home
* Version : 0.0.0.0
* License:
* 	Permission is granted to copy, distribute, and/or modify this document under the terms of the Creative Commons Attribution-NonCommercial 3.0 
* 	Unported License, which is available at http: //creativecommons.org/licenses/by- nc/3.0/.
* Purpose :
------------------------------------------------------
*/

//Add a link to your data object, and use v-bind to sync it up with an anchor tag in your HTML. Hint: you’ll be binding to the href attribute.

var app = new Vue({
  el: '#app',
  data: {
    product: 'Socks',
    image: 'https://www.vuemastery.com/images/challenges/vmSocks-green-onWhite.jpg',
    link: 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=socks'
  } 
})



/**
 * @author Sebastien Dorey
 * @email sebastien.dorey@laposte.net
 * @create date 2019-07-29 02:37:50
 * @modify date 2019-07-29 02:38:46
 * @desc [description] Demo with vue js 2 try to reproduce
 * 	try to understand integration of graph, svg, in vuejs.
	Exemple taken from the web but from scatered sources in the same example page.
	Try to reproduce localy te exploit but alas :-(
	For the time being it is too hoopsy daisy for me.
 */

// The raw data to observe
var stats = [
    { label: 'A', value: 100 },
    { label: 'B', value: 100 },
    { label: 'C', value: 100 },
    { label: 'D', value: 100 },
    { label: 'E', value: 100 },
    { label: 'F', value: 100 }
]

// A resusable polygon graph component
Vue.component('polygraph', {
    props: ['stats'],
    template: '#polygraph-template',
    computed: {
        // a computed property for the polygon's points
        points: function() {
            var total = this.stats.length
            return this.stats.map(function(stat, i) {
                var point = valueToPoint(stat.value, i, total)
                return point.x + ',' + point.y
            }).join(' ')
        }
    },
    components: {
        // a sub component for the labels
        'axis-label': {
            props: {
                stat: Object,
                index: Number,
                total: Number
            },
            template: '#axis-label-template',
            computed: {
                point: function() {
                    return valueToPoint(+this.stat.value + 10,
                        this.index,
                        this.total
                    )
                }
            }
        }
    }
})

// math helper...
function valueToPoint(value, index, total) {
    var x = 0
    var y = -value * 0.8
    var angle = Math.PI * 2 / total * index
    var cos = Math.cos(angle)
    var sin = Math.sin(angle)
    var tx = x * cos - y * sin + 100
    var ty = x * sin + y * cos + 100
    return {
        x: tx,
        y: ty
    }
}

// bootstrap the demo
new Vue({
    el: '#demo',
    data: {
        newLabel: '',
        stats: stats
    },
    methods: {
        add: function(e) {
            e.preventDefault()
            if (!this.newLabel) return
            this.stats.push({
                label: this.newLabel,
                value: 100
            })
            this.newLabel = ''
        },
        remove: function(stat) {
            if (this.stats.length > 3) {
                this.stats.splice(this.stats.indexOf(stat), 1)
            } else {
                alert('Can\'t delete more!')
            }
        }
    }
})
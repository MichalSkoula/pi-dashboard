// onload
window.onload = (event) => {
    document.getElementById('loading').remove();
};
// for sure
setTimeout(() => {
    if (document.getElementById('loading') !== null) {
        document.getElementById('loading').remove();
    }
}, 3000);



Vue.filter('formatKilo', function(value) {
    if (!value) {
        return '';
    }
    value = parseFloat(value.toString());
    return (value / 1000).toFixed(2);
});
Vue.filter('formatPercent', function(value) {
    if (!value) {
        return '';
    }
    value = parseFloat(value.toString());
    return value.toFixed(2);
});
Vue.filter('formatNumber', function(value) {
    if (!value) {
        return '';
    }
    value = parseFloat(value.toString());
    return Math.round(value);
});

var vm = new Vue({
    el: '#app',
    methods: {
        updateData: function(event) {
            // json
            axios.get('data/data.json').then(response => (
                this.ledtech = response.data
            ));
            
            // camera 1
            document.getElementById("ledtech-indoor-cam").src = document.getElementById("ledtech-indoor-cam-a").href = 'data/indoor.jpg?t=' + (new Date().getTime());
            if (typeof this.lightbox.destroy === 'function') {
                this.lightbox.destroy();
            }
            this.lightbox = new SimpleLightbox({elements: 'a.lightbox'});
            // camera 2
            document.getElementById("ledtech-outdoor-cam").src = document.getElementById("ledtech-outdoor-cam-a").href = 'data/outdoor.jpg?t=' + (new Date().getTime());
            if (typeof this.lightbox.destroy === 'function') {
                this.lightbox.destroy();
            }
            this.lightbox = new SimpleLightbox({elements: 'a.lightbox'});
        }
    },
    data: {
        ledtech: {
            indoor_temp: {},
            outdoor_temp: {},
            indoor_pressure: {},
            outdoor_pressure: {}
        },
        lightbox: ''
    },
    mounted: function() {
        this.updateData();

        window.setInterval(() => {
            this.updateData();
        }, 10 * 1000);
    }
});

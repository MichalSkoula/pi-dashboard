// settings 
var use_motion = true; // otherwise, use images from fswebcam


// filters
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
                this.json = response.data
            ));
            
            // if not using motion, update camera images
            if (!use_motion) {
                document.getElementById('indoor-cam').src = document.getElementById('indoor-cam-a').href = this.settings.indoor_cam_url + 't=' + (new Date().getTime());
                document.getElementById('outdoor-cam').src = document.getElementById('outdoor-cam-a').href = this.settings.outdoor_cam_url + '?t=' + (new Date().getTime());
            }
        }
    },
    data: {
        json: {
            indoor_temp: {},
            outdoor_temp: {},
            indoor_pressure: {},
            outdoor_pressure: {}
        },
        settings: {
            indoor_cam_url: use_motion ? location.href.replace(/\/$/, "") + ':8081' : 'data/indoor.jpg',
            outdoor_cam_url: use_motion ? location.href.replace(/\/$/, "") + ':8082' : 'data/outdoor.jpg'
        }
    },
    mounted: function() {
        this.updateData();

        window.setInterval(() => {
            this.updateData();
        }, 10 * 1000);
    }
});

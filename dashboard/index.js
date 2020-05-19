Vue.filter('formatKilo', function(value) {
    if (!value) {
        return '';
    }
    value = parseFloat(value.toString());
    return (value / 1000).toFixed(2);
});

var vm = new Vue({
    el: '#app',
    methods: {
        updateData: function(event) {
            // json
            axios.get('data/ledtech_indoor.json').then(response => (
                this.ledtech_indoor = response.data
            ));
            axios.get('data/lasena.json').then(response => (
                this.lasena = response.data
            ));
            axios.get('data/ledtech_outdoor.json').then(response => (
                this.ledtech_outdoor = response.data
            ));
            
            // camera 1
            document.getElementById("ledtech-cam").src = document.getElementById("ledtech-cam-a").href = 'data/ledtech_indoor.jpg?t=' + (new Date().getTime());
            if (typeof this.lightbox.destroy === 'function') {
                this.lightbox.destroy();
            }
            this.lightbox = new SimpleLightbox({elements: 'a.lightbox'});
            // camera 2
            document.getElementById("arduino-cam").src = document.getElementById("arduino-cam-a").href = 'data/ledtech_outdoor.jpg?t=' + (new Date().getTime());
            if (typeof this.lightbox.destroy === 'function') {
                this.lightbox.destroy();
            }
            this.lightbox = new SimpleLightbox({elements: 'a.lightbox'});
        }
    },
    data: {
        ledtech_indoor: {
            temp: {}
        },
        lasena: {
            temp: {}
        },
        ledtech_outdoor: {
            temp: {}
        },
        lightbox: ''
    },
    mounted: function() {
        this.updateData();

        window.setInterval(() => {
            this.updateData();
        }, 15 * 1000);
    }
});

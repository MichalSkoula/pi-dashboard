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
            axios.get('data/ledtech.json').then(response => (
                this.ledtech = response.data
            ));
            axios.get('data/lasena.json').then(response => (
                this.lasena = response.data
            ));
            axios.get('data/arduino.json').then(response => (
                this.arduino = response.data
            ));
            
            // camera 1
            document.getElementById("ledtech-cam").src = document.getElementById("ledtech-cam-a").href = 'data/ledtech.jpg?t=' + (new Date().getTime());
            if (typeof this.lightbox.destroy === 'function') {
                this.lightbox.destroy();
            }
            this.lightbox = new SimpleLightbox({elements: 'a.lightbox'});
            // camera 2
            document.getElementById("arduino-cam").src = document.getElementById("arduino-cam-a").href = 'data/arduino.jpg?t=' + (new Date().getTime());
            if (typeof this.lightbox.destroy === 'function') {
                this.lightbox.destroy();
            }
            this.lightbox = new SimpleLightbox({elements: 'a.lightbox'});
        }
    },
    data: {
        ledtech: {
            temp: {}
        },
        lasena: {
            temp: {}
        },
        arduino: {
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

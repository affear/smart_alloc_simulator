(function(document) {
    'use strict';

    document.addEventListener('polymer-ready', function() {

        var DEFAULT_ROUTE = "chart";
        var template = document.querySelector('#t');
        //var menuItem = document.querySelector('#menu-item');
        var pages = document.querySelector('#pages');
        var cache = {};
        var ajax;

        template.pages = [{
            title: "Consumption Chart",
            hash: "chart",
            icon: "trending-up",
            url: 'pages/chart_page.html'
        }, {
            title: "Compute Log",
            hash: "compute_log",
            icon: "toc",
            url: 'logs/compute.log'
        }, {
            title: "Scheduler Log",
            hash: "scheduler_log",
            icon: "toc"
        }, {
            title: "Consolidator Log",
            hash: "consolidator_log",
            icon: "toc"
        }, {
            title: "Database Log",
            hash: "database_log",
            icon: "toc"
        }];
        template.pageTitle = template.pages[0];
        template.addEventListener('template-bound', function(e) {
            this.route = this.route || DEFAULT_ROUTE;
            ajax = document.querySelector('#ajax');
        });

        template.menuItemSelected = function(e, detail, sender) {
            if (detail.isSelected) {
                this.async(function() {
                    if (!cache[ajax.url]) {
                        ajax.go();
                    }
                    document.querySelector('core-scaffold').closeDrawer();
                });

            }
        }
        template.onResponse = function(e, detail, sender) {
            var html = detail.response;
            cache[ajax.url] = html; // Primitive caching by URL.
            var pages = document.querySelector('#pages');
            this.injectBoundHTML(html,
                pages.selectedItem.firstElementChild);
        };

    });
})(wrap(document))

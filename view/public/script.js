(function(document) {
    'use strict';

    document.addEventListener('polymer-ready', function() {

		var DEFAULT_ROUTE="graph";
        var template = document.querySelector('#t');
        var menuItem = document.querySelector('paper-item');
        template.pages = [{
            title: "Graph",
            hash: "graph",
            icon: "trending-up"
        }, {
            title: "Compute Log",
            hash: "compute_log",
            icon: "toc"
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
        }
        ];
        template.pageTitle = template.pages[0];
        template.addEventListener('template-bound', function(e) {
            this.route = this.route || DEFAULT_ROUTE;
        });

        template.menuItemSelected = function (e, detail, sender) {
			template.pageTitle = detail.item.label_;
        	if(detail.isSelected){
        		document.querySelector('core-scaffold').closeDrawer();
        	}
        }
    });
})(wrap(document))

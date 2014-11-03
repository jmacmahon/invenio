 /*
 * This file is part of Invenio.
 * Copyright (C) 2015 CERN.
 *
 * Invenio is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of the
 * License, or (at your option) any later version.
 *
 * Invenio is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Invenio; if not, write to the Free Software Foundation, Inc.,
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */

define(['jquery', 'chartjs', 'pie', 'datetimepicker'], function($, Chart) {
    return { draw: function(event, field, rec_id) {
        var now = Date.now();
        var default_time_from = now - (30*24*60*60*1000); // 30 days ago
        var default_time_to = now;

        var draw_pie_chart = function(settings) {
            return function() {
                var ajax_data = {
                    field: settings.field
                };

                if ('rec_id' in settings) {
                    ajax_data.rec_id = settings.rec_id;
                }

                if ( ('time_from' in settings) && ('time_to' in settings) ) {
                    ajax_data.time_from = settings.time_from;
                    ajax_data.time_to = settings.time_to;
                }

                console.log(ajax_data)
                $.ajax(settings.data_url, {data: ajax_data})
                    .done(function(data) {
                        $('#placeholder').css('display', 'none');
                        $('#refresh_button')[0].disabled = false;

                        var colors = ["#7EB26D", "#EAB839", "#6ED0E0", "#EF843C", "#E24D42", "#1F78C1", "#BA43A9", "#705DA0", "#508642", "#CBA300"];

                        var processed_data = [];
                        var total = data[0];
                        var total_in_buckets = 0;
                        for (var i = 0; i < data[1].length; i++) {
                            var value = data[1][i]['doc_count'];
                            var percentage = (100 * value)/(total + 0.0);
                            var label;
                            if (data[1][i].hasOwnProperty('key_as_string')) {
                                label = data[1][i]['key_as_string'];
                            }
                            else {
                                label = data[1][i]['key'] + '';
                            }
                            label += ': ' + Math.round(percentage) + '%';
                            total_in_buckets += value
                            processed_data.push({
                                value: value,
                                label: label,
                                color: colors[i % colors.length]
                            });
                        }
                        var other_value = (total - total_in_buckets)
                        var other_percentage = (100 * other_value)/(total + 0.0);
                        processed_data.push({
                            value: other_value,
                            label: 'Other: ' + Math.round(other_percentage) + '%',
                            color: '#AAAAAA'
                        });
                        var ctx = $('#chart')[0].getContext("2d");
                        var chart = new Chart(ctx).Pie(processed_data, {});
                    });
            };
        };

        var refreshPie = function() {
            var settings = {
                data_url: '/statistics/api/' + event + '/terms',
                field: field,
                rec_id: rec_id
            };

            var time_from_empty_p = $('#time_from')[0].value === '';
            var time_to_empty_p = $('#time_to')[0].value === '';

            if ( !time_from_empty_p && !time_to_empty_p ) {
                var time_from = $('#time_from').data("DateTimePicker").date().valueOf();
                var time_to = $('#time_to').data("DateTimePicker").date().valueOf();
                if ( !isNaN(time_from) && !isNaN(time_to) ) {
                    settings.time_from = time_from;
                    settings.time_to = time_to;
                }
            }

            $('#refresh_button')[0].disabled = true;

            $(draw_pie_chart(settings));
        };

        // Date picker
        $('#time_from').datetimepicker({
            sideBySide: true,
            format: 'YYYY-MM-DD HH:mm'
        });
        $('#time_to').datetimepicker({
            sideBySide: true,
            format: 'YYYY-MM-DD HH:mm'
        });
        $('#refresh_button').bind('click', function() {
            refreshPie();
        });
        refreshPie();
    }};
});

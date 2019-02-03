'use strict';

function initTable(id, tableOptions) {
    var containerId = id + '-handsontable-container';
    var tableHeaderCheckboxId = id + '-handsontable-header';
    var colHeaderCheckboxId = id + '-handsontable-col-header';
    var colWidthCheckboxId = id + '-handsontable-col-width';
    var hiddenStreamInput = $('#' + id);
    var tableHeaderCheckbox = $('#' + tableHeaderCheckboxId);
    var colHeaderCheckbox = $('#' + colHeaderCheckboxId);
    var colWidthCheckbox = $('#' + colWidthCheckboxId);

    var hot;
    var cellAlignment = {};
    var defaultOptions;
    var finalOptions = {};
    var persist;
    var cellEvent;
    var structureEvent;
    var dataForForm = null;
    var getWidth = function() {
        return $('.widget-table_input').closest('.sequence-member-inner').width();
    };
    var getHeight = function() {
        var tableParent = $('#' + id).parent();
        return tableParent.find('.htCore').height() + (tableParent.find('.input').height() * 2);
    };
    var height = getHeight();
    var resizeTargets = ['.input > .handsontable', '.wtHider', '.wtHolder'];
    var resizeHeight = function(height) {
        var currTable = $('#' + id);
        $.each(resizeTargets, function() {
            currTable.closest('.field-content').find(this).height(height);
        });
    };
    function resizeWidth(width) {
        $.each(resizeTargets, function() {
            $(this).width(width);
        });
        var parentDiv = $('.widget-table_input').parent();
        parentDiv.find('.field-content').width(width);
        parentDiv.find('.fieldname-table .field-content .field-content').width('80%');
    }

    try {
        dataForForm = JSON.parse(hiddenStreamInput.val());
    } catch (e) {
        // do nothing
    }

    if (dataForForm !== null) {
        if (dataForForm.hasOwnProperty('first_row_is_column_width')) {
            colWidthCheckbox.prop('checked', dataForForm.first_row_is_column_width);
        }
        if (dataForForm.hasOwnProperty('first_data_row_is_table_header')) {
            tableHeaderCheckbox.prop('checked', dataForForm.first_data_row_is_table_header);
        }
        if (dataForForm.hasOwnProperty('first_col_is_header')) {
            colHeaderCheckbox.prop('checked', dataForForm.first_col_is_header);
        }
        if (dataForForm.hasOwnProperty('cell_alignment')) {
            dataForForm.cell_alignment.forEach(function(item) {
                cellAlignment[item.row + '-' + item.col] = item;
            });
            // cellAlignment = dataForForm.cell_alignment;
        }
    }

    if (!tableOptions.hasOwnProperty('width') || !tableOptions.hasOwnProperty('height')) {
        // Size to parent .sequence-member-inner width if width is not given in tableOptions
        $(window).on('resize', function() {
            hot.updateSettings({
                width: getWidth(),
                height: getHeight()
            });
            resizeWidth('100%');
        });
    }

    persist = function() {
        // var cells_meta = hot.getCellMeta(0, 0);
        // alert(cells_meta);
        hiddenStreamInput.val(JSON.stringify({
            data: hot.getData(),
            cell_alignment: Object.values(cellAlignment),
            first_row_is_column_width: colWidthCheckbox.prop('checked'),
            first_data_row_is_table_header: tableHeaderCheckbox.prop('checked'),
            first_col_is_header: colHeaderCheckbox.prop('checked'),
        }));
    };

    cellEvent = function(change, source) {
        if (source === 'loadData') {
            return; //don't save this change
        }

        persist();
    };

    structureEvent = function(index, amount) {
        resizeHeight(getHeight());
        persist();
    };

    tableHeaderCheckbox.on('change', function() {
        persist();
    });

    colHeaderCheckbox.on('change', function() {
        persist();
    });

    colWidthCheckbox.on('change', function() {
        persist();
    })

    defaultOptions = {
        afterChange: cellEvent,
        afterCreateCol: structureEvent,
        afterCreateRow: structureEvent,
        afterRemoveCol: structureEvent,
        afterRemoveRow: structureEvent,
        // contextMenu set via init, from server defaults
    };

    if (dataForForm !== null && dataForForm.hasOwnProperty('data')) {
        // Overrides default value from tableOptions (if given) with value from database
        defaultOptions.data = dataForForm.data;
    }

    Object.keys(defaultOptions).forEach(function (key) {
        finalOptions[key] = defaultOptions[key];
    });
    Object.keys(tableOptions).forEach(function (key) {
        finalOptions[key] = tableOptions[key];
    });

    hot = new Handsontable(document.getElementById(containerId), finalOptions);
    // add the alignment settings
    hot.updateSettings({
        cell: Object.values(cellAlignment),
        afterSetCellMeta: function (row, col, key, val) {
            // for now save only the className for cell alignment
            if (key == 'className') {
                var cellId = row + '-' + col;
                if (cellAlignment[cellId] == undefined) {
                    cellAlignment[cellId] = {row: row, col: col, className: val};
                }
                else {
                    cellAlignment[cellId][key] = val;
                }
                persist();
            }
        }
    });
    hot.render(); // Call to render removes 'null' literals from empty cells

    // Apply resize after document is finished loading (parent .sequence-member-inner width is set)
    if ('resize' in $(window)) {
        resizeHeight(getHeight());
        $(window).on('load', function() {
            $(window).trigger('resize');
        });
    }
}
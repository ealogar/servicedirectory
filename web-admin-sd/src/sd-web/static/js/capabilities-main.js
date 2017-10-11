/**
 * (c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
 * Reserved.
 *
 * The copyright to the software program(s) is property of Telefonica I+D.
 * The program(s) may be used and or copied only with the express written
 * consent of Telefonica I+D or in accordance with the terms and conditions
 * stipulated in the agreement/contract under which the program(s) have
 * been supplied.
 */

$(document).ready(function() {

    $('.showAddEndModal').click(function() {
        var tdElement = $(this).parent().filter("td");
        var api_name = tdElement.attr('api_name');
        $('#apiNameField').val(api_name);
        $('#environmentTextField').val('production');
        $('#addEndpointModal').modal('toggle');
        $('#myModalLabel').text('Add new Endpoint to ' + api_name);
    });

    $('.showEditCapModal').click(function() {
        var tdElement = $(this).parent().filter("td");
        var api_name = tdElement.attr('api_name');
        var description = tdElement.attr('description');
        var default_version = tdElement.attr('default_version');
        $('#editCapModalLabel').text('Edit capability: ' + api_name);
        $('#apiNameFieldEdit').val(api_name);
        $('#editDescriptionField').val(description);
        $('#editVersionField').val(default_version);
        $('#editCapabilityModal').modal('toggle');
    });

    $('.showRemoveCapModal').click(function() {
        var tdElement = $(this).parent().filter("td");
        var api_name = tdElement.attr('api_name');
        $('#removeCapModalLabel').text('You are going to delete ' + api_name);
        $('#capabilityRemoveField').val(api_name);
        $('#removeCapModal').modal('toggle');
    });

    $('.submitEditForm').click(function() {
        $('#editForm').submit();
    });

    $('.submitAddEndForm').click(function() {
        $('#addEndForm').submit();
    });

    $('.deleteCapability').click(function() {
        $('#removeForm').submit();
    });

    $('.envItem').click(function() {
        var environment = $(this).attr('item');
        $('#environmentTextField').val(environment);
    });

});

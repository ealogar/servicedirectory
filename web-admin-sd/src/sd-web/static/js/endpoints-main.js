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
    $('#editForm').on('submit', function () {
        //console.log('Submiting form....');
    });

    $('.showEditEndModal').click(function() {
        var tdElement = $(this).parent().filter("td");
        var api_name = tdElement.attr('api_name');
        var url = tdElement.attr('url');
        var version = tdElement.attr('version');
        var environment = tdElement.attr('environment');
        var id = tdElement.attr('end_id');
        var ob = tdElement.attr('ob');
        var premium = (tdElement.attr('premium')==='true');
        $('#editEndModalLabel').text('Edit endpoint: ' + api_name);
        $('#apiNameField').val(api_name);
        $('#idEndField').val(id);
        $('#versionField').val(version);
        $('#environmentTextField').val(environment);
        $('#urlField').val(url);
        $('#obField').val(ob);
        $('#premiumField').prop('checked', premium);
        $('#editEndpointModal').modal('toggle');
    });

    $('.submitEditForm').click(function() {
        $('#editForm').submit();
    });

     $('.showRemoveEndModal').click(function() {
        var tdElement = $(this).parent().filter("td");
        var api_name = tdElement.attr('api_name');
        var url = tdElement.attr('url');
        var version = tdElement.attr('version');
        var id = tdElement.attr('end_id');
        $('#removeEndModalLabel').text('You are going to delete the following endpoint: Api Name: '+
                api_name +', Version: ' + version + ', Url: ' + url );
        $('#apiNameRemoveField').val(api_name)
        $('#idEndRemoveField').val(id)
        $('#removeEndModal').modal('toggle');
    });

    $('.deleteEndpoint').click(function() {
        $('#deleteForm').submit();
    });

    $('.envItem').click(function() {
        var environment = $(this).attr('item');
        $('#environmentTextField').val(environment);
    });

});

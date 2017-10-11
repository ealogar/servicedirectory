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

    $("[data-hide]").on("click", function(){
        $(".alert").hide();
        $('input, select').removeAttr('disabled');
    });

    $('#mainForm').on('submit', function () {
        $('input, select').removeAttr('disabled');
    });

    $('.submitMainForm').click(function() {
        $('#mainForm').submit();
    });

    $('.openAlertDialog').click(function() {
        $('.alert').show();
        $('input, select').attr('disabled', 'disabled');
    });

});

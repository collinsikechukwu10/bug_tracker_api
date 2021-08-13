function taskDashboardFunctionalityInit() {
    $(".project-items").height(
        $(window).height() -
        ($("header").outerHeight() +
            $(".project-header").outerHeight() +
            $(".project-details-header").outerHeight() +
            $(".project-column-header").outerHeight() +
            1)
    )

    // Add listener to keep setting height
    $(window).resize(function () {
        $(".project-items").height(
            $(window).height() -
            ($("header").outerHeight() +
                $(".project-header").outerHeight() +
                $(".project-details-header").outerHeight() +
                $(".project-column-header").outerHeight() +
                1)
        )
    })
}

$(document).on("click", ".projects-body .project", function () {
    window.location = $(this).attr("href")
})
$(document).on("click", ".team-menu .team-menu-list .team-menu-list-item", function () {
    window.location = $(this).attr("href")
})

function beforeLastUnderscore(str) {
    let lastIndex = str.lastIndexOf("_")
    return str.substring(0, lastIndex)
}

function afterLastUnderscore(str) {
    let lastIndex = str.lastIndexOf("_")
    return str.substring(lastIndex + 1)
}

function sortByArray(arr, sortList) {
    let newArr = arr.sort(function (a, b) {
        return sortList.indexOf[a.id] > sortList.indexOf[b.id]
    })
    return newArr
}


const NetworkHandler = Object.freeze({

    notifyServerOfPostRequest(requestJSON, endpoint, callback) {
        var contentType, processData;
        if (typeof requestJSON !== "string") {
            processData = false
            contentType = false
        } else {
            processData = true
            contentType = "application/json"
        }
        $.ajax({type: "POST", processData, contentType, url: endpoint, data: requestJSON}).always(
            function (response, status, ajaxResponse) {
                if (status == 200) this.handleContentFromResponse(ajaxResponse, response)
            })
    },
    determineContentType(response) {
        var contentType = (response.getResponseHeader("Content-Type") !== window.undefined) ? response.getResponseHeader("Content-Type") : ""
        contentType = (contentType.indexOf(";") != null) ? contentType.split(";")[0] : contentType;
        return {isHtml: (contentType === "text/html"), isJson: (contentType === "application/json")}
    },

    handleContentFromResponse(ajaxResponse, response) {
        var contentType = this.determineContentType(ajaxResponse)
        if (contentType.isHtml) return response
        else if (contentType.isJson) {
            if (response["response_code"] != 200) {
                if (response["response_message"]) this.getToastMessageHandler.showErrorMessage(response["response_message"])
            } else return response
        } else this.getToastMessageHandler.showErrorMessage("Cannot process response")
    },
    appSpinner: {
        /** LOADER **/
        startSpinner: function (el) {
            !el ? el = 'body' : null;
            var width = $(el).width(), height = $(el).height(),
                svgWidth = width > 400 || height > 400 ? 100 : (38 / 100 * Math.abs(width ? width : 1));
            svgWidth = Math.round(svgWidth);
            var newEl = "<div class='loader-background'><div id='loader' class='m-auto'><svg version='1.1' id='loaderSVG' xmlns='http://www.w3.org/2000/svg' width='" +
                svgWidth + "px' height='" + svgWidth + "px' viewBox='0 0 40 40' enable-background='new 0 0 40 40' xml:space='preserve'>" +
                "<path opacity='0.2' fill='#20c0e7' d='M20.201,5.169c-8.254,0-14.946,6.692-14.946,14.946c0,8.255,6.692,14.946,14.946,14.946" +
                "s14.946-6.691,14.946-14.946C35.146,11.861,28.455,5.169,20.201,5.169z M20.201,31.749c-6.425,0-11.634-5.208-11.634-11.634" +
                "c0-6.425,5.209-11.634,11.634-11.634c6.425,0,11.633,5.209,11.633,11.634C31.834,26.541,26.626,31.749,20.201,31.749z' />" +
                "<path fill='#20c0e7' d='M26.013,10.047l1.654-2.866c-2.198-1.272-4.743-2.012-7.466-2.012h0v3.312h0 C22.32,8.481,24.301,9.057,26.013,10.047z'>" +
                "<animateTransform attributeType='xml' attributeName='transform' type='rotate' from='0 20 20' to='360 20 20'" +
                " dur='0.5s' repeatCount='indefinite' /></path></svg></div></div>";
            $(el).append(newEl);
            $(el).addClass('loader-parent');
        },

        stopSpinner: function () {
            $('.loader-parent').each(function () {
                $('.loader-background').remove();
                $(this).removeClass("loader-parent");
            });
        }
    }
})
const NotificationHandler = Object.freeze({
    showErrorMessage(message) {
        Swal.fire({
            position: 'center',
            icon: 'warning',
            // title: '<div style="color: #caac4b">Error</div>',
            html: `<div style="color: #20c0e7;font-size: 16px">${message}</div>`,
            showConfirmButton: false,
            padding: '3.5rem',
            background: "#fffcfc",
            iconColor: "#E03131",
            timer: 10000,
            showCancelButton: true,
            focusCancel: true,
            cancelButtonText: "Close",
            cancelButtonColor: "#20c0e7"
        })
    },
    showSuccessMessage(message) {
        Swal.fire({
            position: 'center',
            icon: 'success',
            // title: '<div style="color: #caac4b">Error</div>',
            html: `<div style="color: #20c0e7;font-size: 20px">${message}</div>`,
            showConfirmButton: false,
            // padding: '3.5rem',
            background: "#fffcfc",
            // iconColor: "#E03131",
            showCancelButton: true,
            focusCancel: true,
            cancelButtonText: "Close",
            cancelButtonColor: "#20c0e7"
        })
    }
})


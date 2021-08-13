let app = new Vue({
    el: "#app",

    delimiters: ["[[", "]]"],
    data: {
        click: false,
        modals: {
            task: false,
        },
        collapsedMenu: false,
        columns: {
            open: {
                id: 0,
                name: "open",
                tasks: [],
            },
            in_progress: {
                id: 1,
                name: "in_progress",
                tasks: [],
            },
            testing: {
                id: 2,
                name: "testing",
                tasks: [],
            },
            done: {
                id: 3,
                name: "done",
                tasks: [],
            },
        },
        tasks: [
            {
                id: 1,
                index: 0,
                severity: "minor",
                created: new Date(),
                by: "",
                column: "open",
                text: "Modal on small screens overflows and it's impossible to view the entire modal",
                checklists: [
                    {id: 0, text: "Make modal background blue"},
                    {id: 1, text: "Make modal content background white"},
                ],
            },
            {
                id: 2,
                index: 2,
                severity: "normal",
                created: new Date(),
                by: "",
                column: "open",
                text: "Remove right border from page",
                checklists: [{id: 0, text: "make border same color as background"}],
            },
            {
                id: 3,
                index: 1,
                severity: "important",
                created: new Date(),
                by: "",
                column: "open",
                text: "Remove right image from page",
                checklists: [{id: 0, text: "replace image with color"}],
            },
            {
                id: 4,
                index: 0,
                severity: "important",
                created: new Date(),
                by: "",
                column: "in_progress",
                text: "Modal on small screens overflows and it's impossible to view the entire modal",
                checklists: [
                    {id: 0, text: "Make modal background blue"},
                    {id: 1, text: "Make modal content background white"},
                ],
            },
            {
                id: 5,
                index: 2,
                severity: "critical",
                created: new Date(),
                by: "",
                column: "in_progress",
                text: "Remove right border from page",
                checklists: [{id: 0, text: "make border same color as background"}],
            },
            {
                id: 6,
                index: 1,
                severity: "minor",
                created: new Date(),
                by: "",
                column: "in_progress",
                text: "Remove right image from page",
                checklists: [{id: 0, text: "replace image with color"}],
            },
            {
                id: 7,
                index: 0,
                severity: "normal",
                created: new Date(),
                by: "",
                column: "testing",
                text: "Modal on small screens overflows and it's impossible to view the entire modal",
                checklists: [
                    {id: 0, text: "Make modal background blue"},
                    {id: 1, text: "Make modal content background white"},
                ],
            },
            {
                id: 8,
                index: 2,
                severity: "important",
                created: new Date(),
                by: "",
                column: "testing",
                text: "Remove right border from page",
                checklists: [{id: 0, text: "make border same color as background"}],
            },
            {
                id: 9,
                index: 1,
                severity: "critical",
                created: new Date(),
                by: "",
                column: "testing",
                text: "Remove right image from page",
                checklists: [{id: 0, text: "replace image with color"}],
            },
            {
                id: 10,
                index: 0,
                severity: "important",
                created: new Date(),
                by: "",
                column: "done",
                text: "Modal on small screens overflows and it's impossible to view the entire modal",
                checklists: [
                    {id: 0, text: "Make modal background blue"},
                    {id: 1, text: "Make modal content background white"},
                ],
            },
            {
                id: 11,
                index: 2,
                severity: "normal",
                created: new Date(),
                by: "",
                column: "done",
                text: "Remove right border from page",
                checklists: [{id: 0, text: "make border same color as background"}],
            },
            {
                id: 12,
                index: 1,
                severity: "important",
                created: new Date(),
                by: "",
                column: "done",
                text: "Remove right image from page",
                checklists: [{id: 0, text: "replace image with color"}],
            },
        ],
        severity: ["minor", "normal", "important", "critical"],
        currentTask: {},
        changes: {
            remove: false,
            add: false,
            sort: false,
            create: false,
            delete: false,
        },
        people: {
            tester: [],
            developer: [],
            guest: [],
            unassigned: []
        },
        users: [
            {
                id: 1,
                firstName: "Lois",
                lastName: "Yisa",
                role: "tester",
            },
            {
                id: 2,
                firstName: "Ife",
                lastName: "Apampa",
                role: "tester",
            },
            {
                id: 3,
                firstName: "Abiodun",
                lastName: "Afolabi",
                role: "tester",
            },
            {
                id: 3,
                firstName: "Gbemileke",
                lastName: "Ogunbanwo",
                role: "developer",
            },
            {
                id: 4,
                firstName: "Tommy",
                lastName: "O'Peters",
                role: "developer",
            },
            {
                id: 5,
                firstName: "Ikechukwu",
                lastName: "Collins",
                role: "developer",
            },
            {
                id: 6,
                firstName: "Titi",
                lastName: "Odunfa-Adeoye",
                role: "guest",
            },
            {
                id: 7,
                firstName: "Femi",
                lastName: "Akinwale",
                role: "guest",
            },
        ],
        user: {
            id: 3,
            firstName: "Abiodun",
            lastName: "Afolabi",
            role: "tester",
            privilege: "admin",
        },
    },
    computed: {
        modalDisplayed: function () {
            for (let key in this.modals) {
                if (this.modals[key] === true) {
                    return true
                }
            }
            return false
        },
    },
    methods: {
        sortIntoPeople() {
            this.users.forEach((user) => {
                console.log(user)
                this.people[user.membership__name].push(user)
            })
        },
        sortIntoColumns() {
            let columns = {open: [], in_progress: [], testing: [], done: []}
            this.tasks.forEach((task) => {
                columns[task.status].push(task)
            })
            for (let column in columns) {
                columns[column].sort((a, b) => a.index > b.index)

                // console.log(JSON.stringify(columns))
                this.columns[column].tasks = []
                this.$nextTick(function () {
                    this.columns[column].tasks = columns[column]
                })
                // setTimeout(() => {
                //   // this.columns[column].tasks = columns[column]
                // }, 1)
            }
        },
        isEmpty(element) {
            if (typeof element == "object") {
                for (var key in element) {
                    if (element.hasOwnProperty(key)) return false
                }
                return true
            } else if (typeof element == "array") {
                return element.length < 1
            }
        },
        createNewTask() {
            this.currentTask = {
                id: Math.max(...this.tasks.map((task) => task.id)) + 1,
                index: Math.max(...this.columns.open.tasks.map((task) => task.index)) + 1,
                severity: "",
                created: new Date(),
                by: this.user,
                column: "open",
                text: "",
                defaultText: "&nbsp;",
                checklists: [],
            }
            this.modals.task = true
        },
        addNewTask() {
            if (this.currentTask.severity == "") {
                this.currentTask.severity = "normal"
            }
            this.tasks.push(this.currentTask)
            this.sortIntoColumns()
            this.modals.task = false
        },
        changeHandler(payload) {
            // console.log(payload.list)
            payload.list.forEach((item, index) => {
                let id = afterLastUnderscore(item) * 1
                let task = this.tasks.filter((el) => el.id == id)[0]

                task.index = index
                task.column = $($("#" + item).closest(".project-column")).attr("name")

                console.log(task.id + " " + task.column)
            })

            this.sortIntoColumns()
        },
        change(payload) {
            let oldColumnName = beforeLastUnderscore(payload.old[0])
            let oldColumnOrder = payload.old.map((item) => afterLastUnderscore(item))

            let newColumnName = beforeLastUnderscore(payload.new[0])
            let newColumnOrder = payload.new.map((item) => afterLastUnderscore(item))

            let target = afterLastUnderscore($(payload.target).attr("id"))

            let targetTask = this.columns[oldColumnName].tasks.filter((task) => task.id == target * 1)[0]

            this.columns[newColumnName].tasks.push(targetTask)
            sortByArray(this.columns[newColumnName].tasks, newColumnOrder)
            console.log(newColumnOrder)
            console.log(this.columns[newColumnName].tasks.map((task) => task.id))
            this.columns[oldColumnName].tasks = this.columns[oldColumnName].tasks.filter((task) => task.id !== target * 1)

            this.changes.remove = false
            this.changes.add = false
        },
        sort() {
        },
        setTaskCurrent: function (task) {
            if (this.click) {
                this.currentTask = task
                this.modals.task = true
            }
        },
        consoleSomething: function () {
            console.log("something")
        },
        createNewChecklist: function () {
            if (this.currentTask.checklists.length > 0) {
                if (this.currentTask.checklists[this.currentTask.checklists.length - 1].text !== "") {
                    this.currentTask.checklists.push({
                        id: Math.max(...this.currentTask.checklists.map((step) => step.id)) + 1,
                        index: Math.max(...this.currentTask.checklists.map((step) => step.index)) + 1,

                        text: "",
                    })
                }
            } else {
                this.currentTask.checklists.push({id: 0, index: 0, text: ""})
            }
        },
        show(item) {
            console.log(item)
        },
        async initializeData() {
            let projectId = $("main section #projectIdNumber").val()
            let options = {
                method:"get",
                url: `/api/bugtracker/projects/${projectId}`,
                xsrfCookieName: 'XSRF-TOKEN',
                xsrfHeaderName: 'X-XSRF-TOKEN',
            }
            let {data: {data}} = await axios(options).catch(err=>{
                NotificationHandler.showErrorMessage(err)
            })
            console.log(data)


            if (!this.isEmpty(data.members)) this.users = data.members
            if (!this.isEmpty(data.tasks)) this.tasks = data.tasks


        this.sortIntoPeople()
        this.sortIntoColumns()

        }
    },
    mounted() {

    },
    created() {
        taskDashboardFunctionalityInit()
        this.initializeData()
        // Use Sortable
        for (let column in this.columns) {
            $(`#${column}_column .project-items`).sortable({
                connectWith: ".project-items",
                containment: ".project-details-columns",
                revert: 300,
                remove: function (event, ui) {
                    let items = $(this).sortable("toArray")
                    app.changeHandler({
                        event: "remove",
                        list: items,
                        target: ui.item,
                    })
                },
                receive: function (event, ui) {
                    let items = $(this).sortable("toArray")
                    app.changeHandler({
                        event: "add",
                        list: items,
                        target: ui.item,
                    })
                },
                stop: function (event, ui) {
                    let items = $(this).sortable("toArray")
                    app.sort({
                        list: items,
                        target: ui.item,
                    })
                },
                start: function (event, ui) {
                    app.click = false
                },
            })
        }

    },
})


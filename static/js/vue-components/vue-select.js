Vue.component("vue-select", {
  props: {
    values: {
      type: Array,
      default: function () {
        return [
          {
            name: "No",
            value: false,
          },
          {
            name: "Yes",
            value: true,
          },
        ]
      },
    },
    value: {
      type: String,
    },
    defaultText: {
      type: String,
      default: function () {
        return "Select One"
      },
    },
    icon: {
      type: String,
    },
  },
  data() {
    return {
      dropdownActive: false,
      selected: {},
    }
  },
  methods: {
    changeValue: function (value) {
      this.selected = value
      this.$emit("input", value.value)
    },
    isEmpty(obj) {
      return $.isEmptyObject(obj)
    },
  },
  /*html*/
  template: `
                  <div class="custom-select-vue" @click="dropdownActive=!dropdownActive" tabindex="0" @blur="dropdownActive=false">
                      <div class="select-selected-vue" value="selected.value" :class="{bold: isEmpty(this.selected)}"> <i class="far" :class="icon"></i> {{isEmpty(this.selected) ? this.defaultText : selected.name}}</div>
                      <div class="select-items-vue" :class="{'select-hide': !dropdownActive}">
                          <div v-for="value in values" @click="changeValue(value)" :value="value.value">{{value.name}}</div>
                      </div>
                  </div>
                  `,
  created() {
    if (typeof this.value == "undefined" || this.value == "") {
      //
    } else {
      this.selected = this.values.filter((value) => value.value == this.value)[0]
    }
  },
})

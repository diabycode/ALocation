/* 
    Create an object DataTable wich can be used to make a datatable dynamic. 
        - sort table rows by clicking on the table header
        - filter table rows

    A datatable can switch to a dynamic datatable by adding the class 'dynamic' to the table
    element.
    
*/


class DataTable {

    tableSelector = 'table.dynamic';

    constructor () {

        this.tableElement = document.querySelector(this.tableSelector)
        this.tableBody = this.tableElement.querySelector('tbody')
        this.tableHeader = this.tableElement.querySelector('thead')
        this.tableRows = this.tableBody.querySelectorAll('tr')

        this.tableHeaderClick()
    }

    tableHeaderClick () {
        this.tableHeader.querySelectorAll('th').forEach( th => {
            th.addEventListener('click', (e) => {
                const column = e.target.closest('th')

                // clear all sort classes
                this.tableHeader.querySelectorAll('th').forEach( th => {
                    th.classList.remove("sort")
                })

                column.classList.add('sort')
                if (column.classList.contains('asc') ) {
                    column.classList.remove('asc')
                } else {
                    column.classList.add('asc')
                }

                // handle sorting
                this.sort( column.innerText.trim(), column.classList.contains('asc') )

                this.tableHeader.querySelectorAll('th').forEach( th => {
                    if (th.classList.contains("asc") && !th.classList.contains("sort")) {
                        th.classList.remove("asc")
                    }
                })

            })
        })
    }

    /**
     * Sort the table rows by the given target column
     * @param {String} target 
     * @param {Boolean} asc 
     */
    sort (key, asc=false) {
        console.log("Sorting: ", key, asc)

        const tableColumns = this.tableHeader.querySelectorAll('th')

        // table columns index
        const tableColumnsIndex = {};
        tableColumns.forEach( (th, index) => {
            tableColumnsIndex[th.innerText.trim()] = index
        })

        this.tableRows = [...this.tableRows].sort( (a, b) => {

            let aValue = Array.from(a.querySelectorAll("td"))[tableColumnsIndex[key.trim()]].innerText.trim()
            let bValue = Array.from(b.querySelectorAll("td"))[tableColumnsIndex[key.trim()]].innerText.trim()

            if (asc) {
                return aValue.localeCompare(bValue)
            } else {
                return bValue.localeCompare(aValue)
            }
        })
        this.render()

    }

    /**
     * Render the table rows
     */
    render () {

        console.log("Render...")

        this.tableBody.innerHTML = ''

        this.tableRows.forEach( row => {
            this.tableBody.appendChild( row )
        })
    }
}


const table = new DataTable()


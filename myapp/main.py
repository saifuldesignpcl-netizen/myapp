import flet as ft


def main(page: ft.Page):
    page.title = "Sales CRM"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    # --- Data Store (Demo) ---
    leads = [
        {"name": "Rahim Ahmed", "phone": "01700000000", "status": "Hot"},
        {"name": "Karim Chowdhury", "phone": "01800000000", "status": "Warm"},
    ]

    # --- Header Component ---
    header = ft.Container(
        content=ft.Column(
            [
                ft.Text("Salesman CRM", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Hello, Sales Superstar! 👋", size=14, color=ft.Colors.WHITE_70),
            ]
        ),
        bgcolor=ft.Colors.BLUE_600,
        padding=20,
        # এখানে আপডেট করা হয়েছে (top-left, top-right, bottom-right, bottom-left)
        border_radius=ft.BorderRadius(0, 0, 20, 20)
    )

    # --- Dashboard Summary Cards ---
    def stat_card(title, value, color):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=12, color=ft.Colors.GREY_700),
                    ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=color),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            expand=True
        )

    dashboard = ft.Row(
        [
            stat_card("Total Leads", "12", ft.Colors.BLUE),
            stat_card("Deals Done", "৳45,000", ft.Colors.GREEN),
            stat_card("Pending", "4", ft.Colors.ORANGE),
        ],
        spacing=10
    )

    # --- Leads List View ---
    leads_list_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def update_leads_list():
        leads_list_column.controls.clear()
        for item in leads:
            status_color = ft.Colors.RED if item["status"] == "Hot" else ft.Colors.ORANGE
            leads_list_column.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE),
                        title=ft.Text(item["name"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Phone: {item['phone']}"),
                        trailing=ft.Container(
                            content=ft.Text(item["status"], color=ft.Colors.WHITE, size=12),
                            bgcolor=status_color,
                            padding=ft.Padding(8, 4, 8, 4),
                            border_radius=5
                        )
                    )
                )
            )
        page.update()

    # --- Add Lead Form Inputs ---
    name_input = ft.TextField(label="Customer Name", border_radius=8)
    phone_input = ft.TextField(label="Phone Number", keyboard_type=ft.KeyboardType.PHONE, border_radius=8)
    status_dropdown = ft.Dropdown(
        label="Lead Priority",
        options=[
            ft.dropdown.Option("Hot"),
            ft.dropdown.Option("Warm"),
            ft.dropdown.Option("Cold"),
        ],
        border_radius=8
    )

    def add_lead_click(e):
        if name_input.value and phone_input.value:
            leads.append({
                "name": name_input.value,
                "phone": phone_input.value,
                "status": status_dropdown.value or "Warm"
            })
            name_input.value = ""
            phone_input.value = ""
            status_dropdown.value = None
            update_leads_list()

            # SnackBar আপডেট
            snack = ft.SnackBar(content=ft.Text("New Lead Added Successfully!"))
            page.overlay.append(snack)
            snack.open = True
            page.update()
        else:
            snack = ft.SnackBar(content=ft.Text("Please fill name & phone!"))
            page.overlay.append(snack)
            snack.open = True
            page.update()

    add_button = ft.ElevatedButton(
        "Add New Lead",
        on_click=add_lead_click,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
        width=400
    )

    # --- View Layouts ---
    def get_home_view():
        return ft.Container(
            padding=15,
            content=ft.Column(
                [
                    dashboard,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Text("Recent Leads", size=16, weight=ft.FontWeight.BOLD),
                    leads_list_column
                ],
                expand=True
            )
        )

    def get_add_lead_view():
        return ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Add New Client / Lead", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    name_input,
                    phone_input,
                    status_dropdown,
                    ft.Container(height=10),
                    add_button
                ]
            )
        )

    # --- Navigation Tab Control ---
    def on_nav_change(e):
        if e.control.selected_index == 0:
            main_container.content = get_home_view()
        elif e.control.selected_index == 1:
            main_container.content = get_add_lead_view()
        page.update()

    main_container = ft.Container(content=get_home_view(), expand=True)

    # --- Bottom Navigation Bar ---
    nav_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_ADD, label="Add Lead"),
        ]
    )

    # Page Assembly
    page.add(
        header,
        main_container,
        nav_bar
    )

    update_leads_list()


if __name__ == "__main__":
    ft.app(target=main)
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
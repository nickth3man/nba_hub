use leptos::*;

use crate::data::{NavItem, NAV_ITEMS};

#[derive(Clone)]
pub struct TableColumn {
    pub label: String,
    pub description: Option<String>,
    pub class: Option<&'static str>,
}

impl TableColumn {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
            description: None,
            class: None,
        }
    }

    pub fn with_description(mut self, description: impl Into<String>) -> Self {
        self.description = Some(description.into());
        self
    }

    pub fn with_class(mut self, class: &'static str) -> Self {
        self.class = Some(class);
        self
    }
}

#[component]
pub fn AppLayout(children: Children) -> impl IntoView {
    view! {
        <div class="app">
            <AppNav />
            <main>{children()}</main>
        </div>
    }
}

#[component]
pub fn AppNav() -> impl IntoView {
    view! {
        <nav>
            <div class="nav-inner">
                <a class="logo" href="/">"NBA Hub"</a>
                <div class="nav-links">
                    {NAV_ITEMS
                        .iter()
                        .map(|item: &NavItem| {
                            view! { <a href={item.href}>{item.label}</a> }
                        })
                        .collect_view()}
                </div>
            </div>
        </nav>
    }
}

#[component]
pub fn PageHeader(title: String, subtitle: String, callout: Option<String>) -> impl IntoView {
    view! {
        <header class="page-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
            {callout.map(|text| view! { <div class="callout">{text}</div> })}
        </header>
    }
}

#[component]
pub fn Section(id: String, title: String, children: Children) -> impl IntoView {
    view! {
        <section class="section" id={id}>
            <div class="section-title">
                <h2>{title}</h2>
            </div>
            {children()}
        </section>
    }
}

#[component]
pub fn OnThisPage(items: Vec<(String, String)>) -> impl IntoView {
    view! {
        <aside class="toc">
            <strong>"On this page"</strong>
            <ul>
                {items
                    .into_iter()
                    .map(|(id, label)| view! { <li><a href={format!("#{}", id)}>{label}</a></li> })
                    .collect_view()}
            </ul>
        </aside>
    }
}

#[component]
pub fn Badge(text: String) -> impl IntoView {
    view! { <span class="badge">{text}</span> }
}

#[component]
pub fn BeginnerToggle(is_on: ReadSignal<bool>, set_on: WriteSignal<bool>) -> impl IntoView {
    view! {
        <label class="toggle">
            <input
                type="checkbox"
                prop:checked=move || is_on.get()
                on:change=move |ev| set_on.set(event_target_checked(&ev))
            />
            <span>"Beginner mode"</span>
        </label>
    }
}

#[component]
pub fn SeasonSelect(options: Vec<i32>, selected: i32, on_change: Callback<i32>) -> impl IntoView {
    view! {
        <select
            class="input"
            prop:value=selected
            on:change=move |ev| {
                if let Ok(value) = event_target_value(&ev).parse::<i32>() {
                    on_change.call(value);
                }
            }
        >
            {options
                .into_iter()
                .map(|year| view! { <option value={year}>{year}</option> })
                .collect_view()}
        </select>
    }
}

#[component]
pub fn DataTable(columns: Vec<TableColumn>, rows: Vec<Vec<View>>) -> impl IntoView {
    let column_classes: Vec<&'static str> =
        columns.iter().map(|col| col.class.unwrap_or("")).collect();

    view! {
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        {columns
                            .iter()
                            .map(|col| {
                                let class = col.class.unwrap_or("");
                                let description = col.description.clone();
                                view! {
                                    <th class={class}>
                                        <span
                                            class={if description.is_some() { "tooltip" } else { "" }}
                                            title={description.unwrap_or_default()}
                                        >
                                            {col.label.clone()}
                                        </span>
                                    </th>
                                }
                            })
                            .collect_view()}
                    </tr>
                </thead>
                <tbody>
                    {rows
                        .into_iter()
                        .map(|row| {
                            let classes = column_classes.clone();
                            view! {
                                <tr>
                                    {row
                                        .into_iter()
                                        .enumerate()
                                        .map(|(index, cell)| {
                                            let class = classes.get(index).copied().unwrap_or("");
                                            view! { <td class={class}>{cell}</td> }
                                        })
                                        .collect_view()}
                                </tr>
                            }
                        })
                        .collect_view()}
                </tbody>
            </table>
        </div>
    }
}

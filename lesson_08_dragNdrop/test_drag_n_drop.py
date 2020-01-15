"""Тест функциональности Drag'n'Drop для webelement"""
from selenium.webdriver.common.action_chains import ActionChains


def test_drag_n_drop(browser_driver):
    """Добавление документов в корзину"""
    browser_driver.find_element_by_id("custom-drag-avatar").click()  # Прокрутка страницы
    browser_driver.switch_to.frame(0)
    documents = browser_driver.find_elements_by_class_name("document")
    trash = browser_driver.find_element_by_class_name("trash")
    for document in documents:
        ActionChains(browser_driver).drag_and_drop(document, trash).perform()

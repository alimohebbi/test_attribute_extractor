package chan.android.app.pocketnote;


import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import static android.support.test.InstrumentationRegistry.getInstrumentation;
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.Espresso.pressBack;
import static android.support.test.espresso.Espresso.openActionBarOverflowOrOptionsMenu;
import static android.support.test.espresso.contrib.RecyclerViewActions.actionOnItemAtPosition;
import static android.support.test.espresso.action.ViewActions.*;
import static android.support.test.espresso.assertion.ViewAssertions.*;
import static android.support.test.espresso.matcher.ViewMatchers.*;

import chan.android.app.pocketnote.R;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.core.IsInstanceOf;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.is;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class AppTestMigrator_writeilyTest1_1 {

    @Rule
    public ActivityTestRule<chan.android.app.pocketnote.MainActivity> mActivityTestRule = new ActivityTestRule<>(chan.android.app.pocketnote.MainActivity.class);

    @Test
    public void apptestmigrator_writeilytest1_1() {
        onView(withContentDescription("Search")).perform(click());
        
        onView(withText("Add Note")).perform(click());
        
        onView(withId(R.id.editor_$_edittext_title)).perform(replaceText("note"), closeSoftKeyboard());
        
        onView(withId(R.id.editor_$_note_editor)).perform(replaceText("something"), closeSoftKeyboard());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withId(R.id.editor_$_button_pick_color)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[2]/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[3]/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[4]/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[5]/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[6]/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[7]/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[8]/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.LinearLayout[9]/android.widget.TextView")).perform(click());
        
        pressBack();
        
        pressBack();
        
        onView(withContentDescription("Clear query")).perform(click());
        
        onView(withContentDescription("Search")).perform(click());
        
        onView(withId(R.id.notes_menu_$_add)).perform(longClick());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withContentDescription("Clear query")).perform(click());
        
        onView(allOf(withId(R.id.navmenuitem_label), withText("Settings"))).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withId(R.id.settings_$_textview_photo_title)).perform(click());
        
        onView(allOf(withId(R.id.purple_dialog_row_$_textview_item), withText("Choose photo"))).perform(click());
        
        pressBack();
        
        onView(withId(R.id.settings_$_button_pick_color)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.GridView/android.widget.LinearLayout[2]/android.widget.ImageView")).perform(click());
        
        onView(withId(R.id.settings_$_button_rate)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        onView(allOf(withId(R.id.option_row_$_textview_item), withText("By alphabet"))).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView[2]")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView[2]")).perform(click());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withId(R.id.settings_$_button_pick_color)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.GridView/android.widget.LinearLayout[3]/android.widget.ImageView")).perform(click());
        
        onView(withId(R.id.settings_$_button_rate)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        onView(allOf(withId(R.id.option_row_$_textview_item), withText("By color"))).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView[2]")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView[2]")).perform(click());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withId(R.id.settings_$_button_pick_color)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.GridView/android.widget.LinearLayout[4]/android.widget.ImageView")).perform(click());
        
        onView(withId(R.id.settings_$_button_rate)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        pressBack();
        
        onView(withText("Default color")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.GridView/android.widget.LinearLayout[5]/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        onView(withId(R.id.notes_menu_$_add)).perform(longClick());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withContentDescription("Search")).perform(click());
        
        onView(allOf(withId(R.id.navmenuitem_label), withText("Settings"))).perform(click());
        
        onView(withId(R.id.settings_$_button_pick_color)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.GridView/android.widget.LinearLayout[6]/android.widget.ImageView")).perform(click());
        
        onView(withId(R.id.settings_$_button_rate)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        pressBack();
        
        onView(withText("Default color")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.GridView/android.widget.LinearLayout[7]/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        onView(allOf(withId(R.id.option_row_$_textview_item), withText("As grid view"))).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView[2]")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView[2]")).perform(click());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withText("Pocket Note")).perform(click());
        
        onView(withId(R.id.settings_$_button_pick_color)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.GridView/android.widget.LinearLayout[8]/android.widget.ImageView")).perform(click());
        
        onView(withId(R.id.settings_$_button_rate)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        pressBack();
        
        onView(withText("Default color")).perform(click());
        
        pressBack();
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        pressBack();
        
        onView(withText("Master password")).perform(click());
        
        pressBack();
        
        onView(withId(R.id.settings_$_imageview_photo)).perform(click());
        
        pressBack();
        
        onView(withId(R.id.settings_$_textview_display_name_title)).perform(click());
        
        pressBack();
        
        pressBack();
        
        onView(withId(R.id.settings_$_textview_display_name)).perform(click());
        
        pressBack();
        
        pressBack();
        
        onView(withId(R.id.settings_$_textview_photo_title)).perform(click());
        
        pressBack();
        
        pressBack();
        
        onView(withId(R.id.settings_$_button_pick_color)).perform(click());
        
        pressBack();
        
        onView(withId(R.id.settings_$_button_rate)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        pressBack();
        
        onView(withText("Default color")).perform(click());
        
        pressBack();
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Spinner/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        onView(withContentDescription("Search")).perform(click());
        
        }

        private static Matcher<View> childAtPosition(
            final Matcher<View> parentMatcher, final int position) {

        return new TypeSafeMatcher<View>() {
            @Override
            public void describeTo(Description description) {
                description.appendText("Child at position " + position + " in parent ");
                parentMatcher.describeTo(description);
            }

            @Override
            public boolean matchesSafely(View view) {
                ViewParent parent = view.getParent();
                return parent instanceof ViewGroup && parentMatcher.matches(parent)
                        && view.equals(((ViewGroup)parent).getChildAt(position));
            }
        };
    }
    }
